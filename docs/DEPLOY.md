# Deploying Lanternina

Everything below has been run against a real subscription. Where a step could not be automated it says so plainly rather than pretending.

Lanternina has two halves that are deployed separately:

- **the cloud tier** — the parent-facing panel and its API. This document.
- **the device** — the mini-PC in the home, which holds the learner profile, the sealing keys and the scans. It is never provisioned from here; see [HARDWARE.md](HARDWARE.md).

The split is deliberate and is the core of the design: the cloud stores dashboard state; the device decides when work begins. A dashboard write never enqueues work or wakes the house. Approvals are only ever sealed on the device, so neither the operator of the service nor anyone who compromises it can approve content for an adolescent. See [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 1. What gets created

Three resource groups, split by **lifetime** rather than by layer, so that redeploying the application never risks the data.

| Resource group | Holds | Lifetime |
| --- | --- | --- |
| `rg-lanternina-<env>-core` | VNet, private DNS zones, Log Analytics, Container Registry, two managed identities | Long. Survives app redeploys. |
| `rg-lanternina-<env>-data` | Cosmos DB (serverless), Storage queue, private endpoints, Entra External ID directory | Longest. Deleting this loses households, and the parents' ability to sign in. |
| `rg-lanternina-<env>-app` | Container Apps environment, `api`, `worker`, Static Web App | Disposable. Safe to delete and recreate. |

Three rather than one per layer. A group whose only job is to hold a single resource buys nothing, and a group per region buys nothing either: a group's location is metadata about the group, not a constraint on what it can hold. The line worth drawing is the one between what you can rebuild in minutes and what you cannot rebuild at all.

```text
browser ──► Static Web App (westeurope, static assets only)
                │ authenticated fetch
                ▼
          ca-…-api (swedencentral, HTTP scale 0→N, VNet-integrated)
                │                                  ▲
                    │                                  ▲ device-initiated request
                    ▼                                  │ (may wait through cold start)
                  Storage queue ──► ca-…-worker      [ server in the home ]
                │                             (seals approvals; holds the
                ▼ private endpoint             profile and the scans)
          Cosmos DB serverless
```

### Why the region split

Everything is in **swedencentral**. The single exception is the Static Web App, whose Standard SKU is not offered there. `westeurope` is otherwise avoided because it has capacity constraints; a Static Web App is globally distributed, so its region only decides where the metadata lives.

### Why two container apps

They scale on different signals, and conflating them costs money:

- **`api` scales on HTTP.** An incoming request to an app that has scaled to zero triggers activation and *is served* — the platform holds it while the replica starts. Putting a queue in front of an interactive API does not make it faster, it makes it asynchronous: you would have to return `202` and poll.
- **`worker` scales on the queue.** A message can be created only as part of a request initiated by the home server. Dashboard writes never put work on this queue.

Two consequences worth knowing before they surprise you:

- After the last queue message the worker stays up for a **300 second cool-down** before returning to zero. That is KEDA behaviour, not a bug — but it is on the bill.
- A home-server request may remain open while the API scales from zero. It is occasional work chosen locally, not a permanent long-poll and not traffic caused by a parent write. HTTP ingress times out after **240 seconds**; longer work must persist a correlated result for the home server to retrieve when it contacts the API again.

---

## 2. Prerequisites

| | |
| --- | --- |
| Azure CLI | 2.86 or newer (`az version`) |
| PowerShell | 7+ on Windows, or `pwsh` on Linux/macOS |
| Permissions | **Owner** *and* **User Access Administrator** on the target subscription |

The second permission is not optional and is the usual place a first attempt fails: the templates create role assignments (managed identity → registry, → Cosmos data plane, → queue). `Contributor` alone cannot write role assignments.

Check yours:

```powershell
az role assignment list --assignee <your-upn> --include-inherited --query "[].roleDefinitionName" -o tsv
```

---

## 3. Deploy

```powershell
git clone https://github.com/faustinopalma/lanternina.git
cd lanternina

# Signs in with a device code into a workspace-local, gitignored CLI profile.
./scripts/deploy.ps1 -Login

# See the plan without changing anything.
./scripts/deploy.ps1 -WhatIf

# Do it.
./scripts/deploy.ps1 -SubscriptionId <guid> -Owner <you> -BudgetContactEmail <you@example.com>
```

The script is **idempotent**: run it as many times as you like.

### The CLI session is isolated on purpose

`scripts/deploy.ps1` sets `AZURE_CONFIG_DIR` to `.azure/` inside the repository, which is gitignored. Signing in here does **not** disturb `az` sessions in your other terminals, and signing out elsewhere does not break this one. If you run `az` commands by hand against this deployment, set the same variable first:

```powershell
$env:AZURE_CONFIG_DIR = "$PWD/.azure"
```

### Parameters

Committed defaults live in [infra/main.bicepparam](../infra/main.bicepparam). The three values that are *not* committed — subscription, owner, budget contact — are passed on the command line, because they are specific to whoever is deploying.

| Parameter | Default | Notes |
| --- | --- | --- |
| `projectName` | `lanternina` | Part of every resource name. |
| `environmentName` | `dev` | Deploy `prod` alongside `dev` without collisions. |
| `location` | `swedencentral` | Everything except the Static Web App. |
| `webLocation` | `westeurope` | Static Web App only. |
| `dataPublicNetworkAccess` | `Disabled` | See §5. |
| `deployExternalId` | `true` | Set `false` to reuse an existing directory. |
| `externalIdDomainPrefix` | derived | **Maximum 10 characters** — see §4. |
| `monthlyBudgetAmount` | `50` | Alerts at 50 / 80 / 100 per cent. |

Resource names end in a five-character hash of the subscription id plus project and environment. It is deterministic, so redeploys are stable, and it is different per subscription, so two forks never collide on a globally unique name.

### The panel in the browser

`deploy.ps1` creates the Static Web App; it does not fill it. The panel is a React application in [web/](../web), built with Vite into `web/dist`, and published by [.github/workflows/panel.yml](../.github/workflows/panel.yml) on any push to `main` that touches `web/`. The workflow runs the component tests and `tsc` before publishing, so a type error stops the release rather than shipping.

It needs one repository secret, `AZURE_STATIC_WEB_APPS_API_TOKEN`, which is the site's deployment token:

```powershell
az staticwebapp secrets list --name <staticWebAppName> --query "properties.apiKey" -o tsv
```

To publish by hand, or to look at the panel locally:

```powershell
cd web
npm ci
npm run dev      # http://localhost:5173
npm run build    # web/dist, including staticwebapp.config.json
```

`http://localhost:5173/?preview` opens the panel against a fake API with invented content, so the layout can be looked at without an identity provider and without a household. It exists only in the dev server: the branch is behind `import.meta.env.DEV` and no fixture text appears in `web/dist`.

`web/public/staticwebapp.config.json` carries the content security policy. It allows scripts from this origin only — the identity library comes from npm, not a CDN — and `blob:` images, because a picture is fetched with the bearer token and handed to the `<img>` as a blob URL.

### The house on a new card

The other half is a Raspberry Pi in the room, and until 24 August 2026 nothing said what it needed. The hub had been built by hand over three weeks; the knowledge of which packages had been installed and which of the seventeen units mattered lived in one filesystem. That is the porting problem, and [deploy/hub-install.sh](../deploy/hub-install.sh) is the answer to it — the declared list, and a check that says whether a machine has it.

Measured on the hub, aarch64 Debian 13, on 24 August 2026: nine packages on top of a Raspberry Pi OS base, whose recursive dependency closure is **597 packages and 1378 MB installed**. The card is 14 GB with 5.3 GB free.

```bash
# On a machine with the repository:
git archive HEAD devices shared orchestrator printing vision experiences -o lanternina.tar
scp lanternina.tar deploy/hub-install.sh deploy/lanternina-* pi@newhub.local:/tmp/

# On the card, as root:
cd /tmp && ./hub-install.sh --install /tmp/lanternina.tar
#   → installs the packages, the tree as root:root 644, the units, and enables the timers.
#   → does NOT write /etc/lanternina: see below.
./hub-install.sh --check
```

The tar is what `git archive` holds rather than the working copy, so the file on the card is the committed file: this machine checks out CRLF and the hub keeps LF, and a plain copy would differ from the commit in every line while being functionally identical.

**Four environment files are not written by the script, on purpose.** They carry the device key and the household id, and the household id has no second copy — it names the rows in Cosmos. A script that invented them would produce a house that starts and then fails for a reason nobody can see, so `--check` names each file and each variable it must set instead:

| File | Sets |
| --- | --- |
| `panel.env` | `LANTERNINA_PANEL_URL`, `LANTERNINA_HOUSEHOLD`, `LANTERNINA_DEVICE_KEY` |
| `experience.env` | `LANTERNINA_EXPERIENCE`, `LANTERNINA_PRINTER` |
| `scanner.env` | `LANTERNINA_SHEETS_DIR`, `LANTERNINA_SCANNER` |
| `trmnl-byos.env` | `TRMNL_BASE_URL`, `TRMNL_SCREEN_FILE`, `TRMNL_DEVICE_REGISTRY`, `TRMNL_PORT`, `LANTERNINA_JOBS_FILE` |

Three things the card must also have, and none of them is Python: a CUPS queue pointing at the printer, `sane-airscan` able to see the scanner over the network, and `avahi-daemon` running — the display resolves `lanternina.local` by mDNS, which the machine answers and the code does not. The printer and the scanner are reached by address, so they are configuration of the room rather than of the card.

[deploy/install-trmnl-byos.sh](../deploy/install-trmnl-byos.sh) predates this and does the display half of the same job. It is what installed the running hub and is left where it is; on a new card `hub-install.sh` covers all of it, and running both expecting different trees is how they would drift.

**What is verified and what is not.** `--check` was run against the working hub and found nothing, and then run again with a package name that does not exist and a variable that is not set, where it reported both and exited 1. `--install` has never been run: doing that takes a second card, and a script that has only ever been read is not a script that works.

**Whether the hub is behind** is a separate question with its own answer, [scripts/hub-stale.ps1](../scripts/hub-stale.ps1): it compares the git blob content of every package the hub runs against what is on the machine. Until 24 August 2026 it compared two directories and reported a clean hub while `orchestrator/` was missing altogether.

**Why this is not a container image.** It was considered on 24 August 2026 and deferred, with the numbers above as the reason. An image would carry the same 1378 MB, would need building for arm64 and pulling onto a card with 5.3 GB free, and would run a `podman` per oneshot for a unit that fires once a minute and costs 1.1 s of CPU. It would also give up most of what a container is for: `lp`, `scanimage` and `avahi-browse` reach cupsd, the scanner and the avahi socket, so the container would want host networking and the host's D-Bus, while the units already have `ProtectSystem=strict` and `ReadOnlyPaths=/opt/lanternina`. What it would buy is Python dependency versions independent of Debian's, and one artefact instead of two steps. The answer changes when there is a second machine or a platform that is not Debian.

---

## 4. Entra External ID

The directory **is created by the deployment** — it is a real ARM resource (`Microsoft.AzureActiveDirectory/ciamDirectories`), so no manual portal step is needed to bring the tenant into existence.

> ⚠️ **The resource name is `<prefix>.onmicrosoft.com` and ARM caps it at 26 characters**,
> so the prefix cannot exceed **10**. This is not in the documentation; the Bicep compiler
> is what caught it. A longer prefix fails at deploy time.
> ⚠️ **`countryCode` sets data residency and cannot be changed afterwards.** Choose it
> deliberately.

### What ARM does *not* create — you must do this yourself

Everything *inside* the directory is tenant-scoped and outside ARM's reach. These four steps are the **entire manual surface of a deployment**; everything else in this document is scripted.

Do them in this order. Steps 1 and 2 come first because a redirect URI is matched exactly — register the generated Static Web App hostname now and you will redo both the app registration and the front end when the real domain arrives.

#### 1. Point the domain at the Static Web App *(your DNS provider)*

Add a `CNAME` for the hostname you intend to use, pointing at the deployment's `staticWebAppHostname` output.

> ⚠️ **If your DNS is behind a proxy — Cloudflare's orange cloud, or equivalent — turn it
> off for this record.** Azure validates ownership and renews the certificate by resolving
> the name to the static web app over the public internet. A proxy answers with its own
> addresses, and the failure is not an error today: it is a certificate that silently fails
> to renew in about three months. Static Web Apps already provides a global CDN and a free
> auto-renewed certificate, so a proxy in front duplicates the one and endangers the other.

#### 2. Add the custom domain *(Azure portal)*

Static Web App → **Custom domains** → **+ Add** → **Custom domain on other DNS**. Add the `TXT` record it asks for, and wait for the status to read **Ready** before continuing. The certificate is issued automatically.

#### 3. Register the application *(Entra admin centre, external tenant)*

Sign in at `entra.microsoft.com` and switch directory to the external tenant.

- **App registrations → New registration**, accounts in this directory only.
- Platform **Single-page application**, redirect URI = `https://<your-domain>`.
- **Expose an API**: accept the default Application ID URI, add a scope.
- **API permissions**: add that scope from *My APIs*, then grant admin consent.

#### 4. Create the user flow and attach the app *(same place)*

**External Identities → User flows → New user flow**. Include **Email** among the attributes returned, since the panel shows it to whoever approves the account. Then, inside the flow, **Applications → Add application**.

#### Then feed two values back to the deployment

| Value | Where it goes |
| --- | --- |
| Application (client) ID | `panelOidcAudience` |
| Authority URL for the tenant | `panelOidcAuthority` |

> **Read the audience, do not derive it.** Sign in once, decode the access token, and use
> the `aud` claim verbatim. The verifier compares it literally, and a guess produces a 401
> that looks like a credentials problem and is not one.

These four steps are also precisely why moving to a new tenant is a **rebuild, not a migration** — see §6. They are scriptable through Microsoft Graph, which is the obvious next improvement; until that exists, this list is the whole of it.

### The administrator, who is not in this directory

A parent who signs up lands in `pending` and stays there until someone admits them. That someone signs in against the **workforce tenant** — the directory that administers the subscription — and not against the External ID directory above.

The reason is the shape of the two directories. External ID exists so that anyone may register themselves; an administrator defined there would be an administrator whose identity came from a public form. Holding the privilege in the workforce tenant also puts it outside the database it edits, so no fault in the code that admits parents can grant it, and it brings the conditional access and multi-factor policies the external directory does not have. What it costs: a second application to register, and an administrator who cannot try the parent experience with the account they already hold.

Like the four steps above, this is done by hand, once, in the **Entra admin centre** of the workforce tenant. It is identity configuration, not infrastructure: ARM does not create it, a redeployment does not restore it, and a script that wrapped it would be a second place for it to drift.

##### 1. Register the application

**Applications → App registrations → New registration**

| Field | Value |
| --- | --- |
| Name | `Lanternina Administration` |
| Supported account types | Accounts in **this organizational directory only** |
| Redirect URI | **Single-page application (SPA)** · `https://app.lanternina.com/admin` |

Add `http://localhost:5173/admin` as a second SPA redirect if you want to run the page locally. Write down the **Application (client) ID** and the **Directory (tenant) ID**.

##### 2. Expose the scope

**Expose an API → Application ID URI → Add**. The portal proposes `api://<application (client) id>` — the id of *this* application, already filled in. Accept it and **Save**; there is nothing to type and no other application's id belongs here.

> The application points at itself because it plays two roles: the page in the browser is
> the client, the panel API is the resource. OAuth has no notion of "the same app", so the
> resource role has to be named before the client role can ask for a token addressed to
> it. The parent's application has exactly the same shape.

Then **+ Add a scope**:

| Field | Value |
| --- | --- |
| Scope name | `access_as_admin` |
| Who can consent? | **Admins only** |
| Admin consent display name | Administer Lanternina |
| Admin consent description | Allows the administration page to call the panel API on behalf of the signed-in administrator. |
| State | **Enabled** |

> **The scope names the API, not the function.** What an administrator may do is decided
> by app roles, which is what the API checks; the scope only makes Entra address the token
> to us. A scope per function — `admit_accounts`, then another one next year — would read
> like a permission boundary and would not be one, because `scp` is not verified anywhere.
> The parent's application is the same shape: one `access_as_parent`, and the account
> record decides the rest.

##### 3. Set the token version to 2

**Manifest** → in *Microsoft Graph App Manifest*, inside the `api` object, change `"requestedAccessTokenVersion": null` to `2` → **Save**. In the older *AAD Graph* manifest the same field is at the top level and is called `accessTokenAcceptedVersion`.

> This one is easy to skip and fails in a way that reads like a credentials problem. Left
> at the default the tenant issues a version 1 token, whose `iss` is
> `https://sts.windows.net/<tenant>/` — and the API takes its issuer from the v2 discovery
> document, so every sign-in ends in a refusal that says nothing about why.
>
> It is also what makes the `aud` claim the bare client id rather than the `api://` form,
> which is why `panelAdminOidcAudience` below carries both.

##### 4. Create the role

**App roles → + Create app role**

| Field | Value |
| --- | --- |
| Display name | `Lanternina administrator` |
| Allowed member types | **Users/Groups** |
| Value | `Lanternina.Admin` |
| Description | Administers Lanternina. Today that is admitting or refusing parent sign-ups, and it grants no access to any household's data. |
| Do you want to enable this app role? | ticked |

`Value` is the string the API compares literally. A typo here is a role nobody holds.

One role for now. A second capability that not every administrator should hold is a second app role, not a second scope: the role is the thing the API already checks.

##### 5. Ask for the scope, and consent to it

**Manage → API permissions → + Add a permission → My APIs → Lanternina Administration → Delegated permissions → `access_as_admin` → Add permissions**. Then **Grant admin consent for &lt;tenant&gt;** and confirm: the row must end up green, *Granted for &lt;tenant&gt;*.

Both lists are needed and they are different halves of the same agreement: `API permissions` is the client role saying what it will ask for, and the consent is the administrator agreeing in advance on behalf of the directory. Remove the `User.Read` permission the portal adds by default — the page never calls Microsoft Graph.

##### 6. Assign the role, and require assignment

**Applications → Enterprise applications → Lanternina Administration → Users and groups →
+ Add user/group** → *Users: None Selected* → pick yourself → **Select** → under *Select a role* choose **Lanternina administrator** → **Assign**.

> **Check the role that was actually assigned.** The portal will happily record an
> assignment to *Default Access*, which is an assignment carrying no role — it is what you
> get by adding the user before the role exists, or by leaving the selector alone. The
> resulting token is valid in every respect and has no `roles` claim, so the API refuses it
> and the refusal reads like a credentials problem. Seen once here, on the first attempt.
> To confirm from outside the portal:
>
> ```powershell
> az rest --method GET --uri "https://graph.microsoft.com/v1.0/servicePrincipals/<sp id>/appRoleAssignedTo"
> ```
>
> An `appRoleId` of all zeros is *Default Access*. Remove the assignment and add it again.

Then **Properties → Assignment required? → Yes → Save**, so a colleague who is not an administrator is stopped at sign-in rather than after it.

> **The application existing grants nothing.** A token without `Lanternina.Admin` in its
> `roles` claim is refused with the same body as any other refusal.

##### Then feed five values back

Three to the API, on the next deployment:

| Value | Where it goes |
| --- | --- |
| `https://login.microsoftonline.com/<tenant id>/v2.0` | `panelAdminOidcAuthority` |
| `<client id>,api://<client id>` | `panelAdminOidcAudience` |
| `Lanternina.Admin` | `panelAdminRole` |

Two are read at build time by the administration page. Locally they go in `web/.env.local`, which is gitignored because it names the tenant:

```
VITE_ADMIN_CLIENT_ID=<client id>
VITE_ADMIN_TENANT_ID=<tenant id>
```

For the published site they are **repository variables** of the same names, under *Settings → Secrets and variables → Actions → Variables*. Variables and not secrets: both values end up in a bundle anybody can read, so hiding them would only make them harder to correct. They are kept out of the repository so a fork does not carry this tenant.

Without them the page at `/admin` loads and says it is not configured, which is the intended closed position.

---

## 4b. The API rolls out from a push, and there is no secret for it

`.github/workflows/api.yml` builds the image and moves the container app onto it. What signs it in is a **user-assigned managed identity**, `id-lanternina-github` in `rg-lanternina-dev-core`, with a federated credential rather than a password.

There is nothing to rotate and nothing to leak. GitHub mints a short-lived token that says *this is the repository `faustinopalma/lanternina`, on `refs/heads/main`*; Entra trades it for a token belonging to the identity, but only because a federated credential names that exact subject. A copy of the workflow in a fork, or on another branch, gets a token Entra refuses.

⚠️ **The subject carries numeric ids, not names, and getting this wrong is the whole failure.** The first attempt registered `repo:faustinopalma/lanternina:ref:refs/heads/main` and Entra answered `AADSTS700213: No matching federated identity record found for presented assertion subject`, naming what had actually arrived:

```
repo:faustinopalma@39453908/lanternina@1338031850:ref:refs/heads/main
```

Do not write that by hand from this file. Add the credential, run the workflow once, and **read the subject out of the error** — it is quoted in full, and it is the only source that cannot be out of date. The id form is the better one anyway: it survives the repository being renamed, which the name form does not.

The three values in *Settings → Secrets and variables → Actions → Variables* are a client id, a tenant id and a subscription id. They are variables and not secrets for the same reason as above and a better one: none of them is a credential. On their own they open nothing, and reading them in a log is what makes a failed sign-in diagnosable.

**What the identity may do, which is the whole of it:**

| role | scope |
| --- | --- |
| `AcrPush` | the registry `acrlanterninadevssveb` |
| `Reader` | the same registry — `az acr login` resolves the login server through ARM, and `AcrPush` carries no control-plane read |
| `Container Apps Contributor` | the single app `ca-lanternina-dev-api` |

It cannot read a secret, cannot delete the registry, and cannot touch `ca-lanternina-dev-worker` beside it. To see it as it is rather than as this file claims:

```powershell
az role assignment list --assignee 8144796a-f04f-434c-9483-9c3ee5912471 --all -o table
az identity federated-credential list --identity-name id-lanternina-github -g rg-lanternina-dev-core -o table
```

**Why the image is built on the runner and not with `az acr build`.** `AcrPush` grants `pull/read` and `push/write`. `az acr build` queues a task on the registry and needs `scheduleRun`, which among the built-in roles only `Contributor` carries — so keeping the familiar command would have meant an identity that can also reconfigure or delete the registry, for the same image. Building on the runner also puts the build log in the run, instead of the `--no-logs` that works around the CLI crash described in §Troubleshooting.

**To take it away**, delete the identity; the assignments and the credential go with it, and the workflow starts failing at sign-in rather than doing something unexpected:

```powershell
az identity delete --name id-lanternina-github --resource-group rg-lanternina-dev-core
```

⚠️ Created by CLI and **not yet described in `infra/`**. A redeploy of `main.bicep` will not remove it, but nothing in the templates would recreate it either.

---

## 5. The data tier is private by default

Cosmos DB and the storage account ship with `publicNetworkAccess = Disabled` and are reachable only through private endpoints from inside the Container Apps environment.

The consequence, which you will hit within five minutes of development: you cannot query Cosmos from your laptop. That is intended. Two ways forward:

- **Preferred** — never let a browser or a laptop touch the data tier directly. The API proxies what it needs to, using its managed identity. This is also why the sheet preview is streamed through our own endpoint rather than handed out as a SAS URL: an SVG can carry a `<script>`, and serving it from our origin lets us apply a content security policy.
- **When you genuinely need direct access** — redeploy with `-p dataPublicNetworkAccess=Enabled`, do the work, then set it back. The private endpoints are created either way, so nothing else changes.

**No keys anywhere.** Cosmos has `disableLocalAuth: true`, the storage account has `allowSharedKeyAccess: false`, and the registry has the admin user disabled. Everything authenticates with the managed identity. Cosmos keys in particular cannot be scoped down, so a leaked one gives full access.

### A note for the MCAPS-style subscriptions

If you deploy into a Microsoft-sponsored subscription, you may have read that public endpoints are forbidden. Checked against the actual policy set on 6 Aug 2026: the deny initiative contains eleven policies and **none of them concerns `publicNetworkAccess`** — it is covered by an *audit* initiative. You are therefore not blocked on day one, but audit findings are still findings, and the posture above is the right one anyway.

---

## 6. Moving to a different subscription or tenant

This is designed for. No tenant id, subscription id, object id or email appears anywhere in `infra/`.

**A different subscription** is a redeploy: point the script at the new one.

**A different tenant is a rebuild, not a migration.** Identities do not move. You will recreate:

- the app registrations (their client ids change)
- the External ID user flows and the accounts inside them
- every managed identity — and therefore every role assignment, including the Cosmos data-plane ones that reference principal ids

The templates handle all of that automatically. What does not come along is the *contents* of the old External ID directory: accounts must be created again. Plan for it rather than discovering it.

Data in Cosmos is a separate export/import exercise and is out of scope here.

---

## 7. Verifying a deployment

```powershell
$env:AZURE_CONFIG_DIR = "$PWD/.azure"

# Everything tagged as ours, and nothing else.
az resource list --tag project=lanternina --query "[].{name:name,type:type,rg:resourceGroup}" -o table

# The data tier really is closed.
az cosmosdb list -g rg-lanternina-dev-data --query "[].{n:name,public:publicNetworkAccess,localAuth:disableLocalAuth}" -o table
az storage account list -g rg-lanternina-dev-data --query "[].{n:name,public:publicNetworkAccess,sharedKey:allowSharedKeyAccess}" -o table

# The API answers.
$fqdn = az containerapp show -n ca-lanternina-dev-api -g rg-lanternina-dev-app --query properties.configuration.ingress.fqdn -o tsv
curl "https://$fqdn/"
```

The first request after an idle period pays a cold start, because `minReplicas` is zero. That is the intended trade: no traffic, no bill.

---

## 8. Tearing it down

```powershell
az group delete -n rg-lanternina-dev-app --yes      # disposable
az group delete -n rg-lanternina-dev-core --yes
az group delete -n rg-lanternina-dev-data --yes     # ⚠️ households, and the directory
```

Deleting the data resource group deletes the External ID directory and every account in it, along with the households in Cosmos. There is no undo.

---

## 9. Things that will bite you

Collected from doing this, not from documentation.

- **`az acr build` crashes on Windows** with `UnicodeEncodeError` while streaming build logs through the console's default encoding. The server-side build *succeeds* and pushes the image; only the local process dies, so any later step in your script is silently skipped. Use `--no-logs`, or set `$env:PYTHONUTF8 = '1'` first.
- **PowerShell eats `||` inside a JMESPath `--query`**, even between double quotes: the argument is truncated at the first `||`. Filter with `Select-String` instead.
- **Import the base image into your registry** (`az acr import`) rather than pulling from Docker Hub on every build, or you will meet the anonymous rate limit at the worst moment.
- **Keep the registry in the same region as the Container Apps environment.** Image pull time is a large part of cold start.
- **Log Analytics is the quiet cost driver**, not Cosmos. The template caps retention at 30 days and daily ingestion at 1 GB. Raise it deliberately, not by accident.
