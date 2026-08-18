# Deploying Lanternina

Everything below has been run against a real subscription. Where a step could not be
automated it says so plainly rather than pretending.

Lanternina has two halves that are deployed separately:

- **the cloud tier** — the parent-facing panel and its API. This document.
- **the device** — the mini-PC in the home, which holds the learner profile, the sealing
  keys and the scans. It is never provisioned from here; see [HARDWARE.md](HARDWARE.md).

The split is deliberate and is the core of the design: the cloud stores dashboard state;
the device decides when work begins. A dashboard write never enqueues work or wakes the
house. Approvals are only ever sealed on the device, so neither the operator of the service
nor anyone who compromises it can approve content for an adolescent. See
[ARCHITECTURE.md](ARCHITECTURE.md).

---

## 1. What gets created

Three resource groups, split by **lifetime** rather than by layer, so that redeploying the
application never risks the data.

| Resource group | Holds | Lifetime |
| --- | --- | --- |
| `rg-lanternina-<env>-core` | VNet, private DNS zones, Log Analytics, Container Registry, two managed identities | Long. Survives app redeploys. |
| `rg-lanternina-<env>-data` | Cosmos DB (serverless), Storage queue, private endpoints, Entra External ID directory | Longest. Deleting this loses households, and the parents' ability to sign in. |
| `rg-lanternina-<env>-app` | Container Apps environment, `api`, `worker`, Static Web App | Disposable. Safe to delete and recreate. |

Three rather than one per layer. A group whose only job is to hold a single resource buys
nothing, and a group per region buys nothing either: a group's location is metadata about
the group, not a constraint on what it can hold. The line worth drawing is the one between
what you can rebuild in minutes and what you cannot rebuild at all.

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

Everything is in **swedencentral**. The single exception is the Static Web App, whose
Standard SKU is not offered there. `westeurope` is otherwise avoided because it has
capacity constraints; a Static Web App is globally distributed, so its region only decides
where the metadata lives.

### Why two container apps

They scale on different signals, and conflating them costs money:

- **`api` scales on HTTP.** An incoming request to an app that has scaled to zero triggers
  activation and *is served* — the platform holds it while the replica starts. Putting a
  queue in front of an interactive API does not make it faster, it makes it asynchronous:
  you would have to return `202` and poll.
- **`worker` scales on the queue.** A message can be created only as part of a request
  initiated by the home server. Dashboard writes never put work on this queue.

Two consequences worth knowing before they surprise you:

- After the last queue message the worker stays up for a **300 second cool-down** before
  returning to zero. That is KEDA behaviour, not a bug — but it is on the bill.
- A home-server request may remain open while the API scales from zero. It is occasional
  work chosen locally, not a permanent long-poll and not traffic caused by a parent write.
  HTTP ingress times out after **240 seconds**; longer work must persist a correlated result
  for the home server to retrieve when it contacts the API again.

---

## 2. Prerequisites

| | |
| --- | --- |
| Azure CLI | 2.86 or newer (`az version`) |
| PowerShell | 7+ on Windows, or `pwsh` on Linux/macOS |
| Permissions | **Owner** *and* **User Access Administrator** on the target subscription |

The second permission is not optional and is the usual place a first attempt fails: the
templates create role assignments (managed identity → registry, → Cosmos data plane,
→ queue). `Contributor` alone cannot write role assignments.

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

`scripts/deploy.ps1` sets `AZURE_CONFIG_DIR` to `.azure/` inside the repository, which is
gitignored. Signing in here does **not** disturb `az` sessions in your other terminals, and
signing out elsewhere does not break this one. If you run `az` commands by hand against
this deployment, set the same variable first:

```powershell
$env:AZURE_CONFIG_DIR = "$PWD/.azure"
```

### Parameters

Committed defaults live in [infra/main.bicepparam](../infra/main.bicepparam). The three
values that are *not* committed — subscription, owner, budget contact — are passed on the
command line, because they are specific to whoever is deploying.

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

Resource names end in a five-character hash of the subscription id plus project and
environment. It is deterministic, so redeploys are stable, and it is different per
subscription, so two forks never collide on a globally unique name.

### The panel in the browser

`deploy.ps1` creates the Static Web App; it does not fill it. The panel is a React
application in [web/](../web), built with Vite into `web/dist`, and published by
[.github/workflows/panel.yml](../.github/workflows/panel.yml) on any push to `main` that
touches `web/`. The workflow runs the component tests and `tsc` before publishing, so a
type error stops the release rather than shipping.

It needs one repository secret, `AZURE_STATIC_WEB_APPS_API_TOKEN`, which is the site's
deployment token:

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

`http://localhost:5173/?preview` opens the panel against a fake API with invented content,
so the layout can be looked at without an identity provider and without a household. It
exists only in the dev server: the branch is behind `import.meta.env.DEV` and no fixture
text appears in `web/dist`.

`web/public/staticwebapp.config.json` carries the content security policy. It allows
scripts from this origin only — the identity library comes from npm, not a CDN — and `blob:`
images, because a picture is fetched with the bearer token and handed to the `<img>` as a
blob URL.

---

## 4. Entra External ID

The directory **is created by the deployment** — it is a real ARM resource
(`Microsoft.AzureActiveDirectory/ciamDirectories`), so no manual portal step is needed to
bring the tenant into existence.

> ⚠️ **The resource name is `<prefix>.onmicrosoft.com` and ARM caps it at 26 characters**,
> so the prefix cannot exceed **10**. This is not in the documentation; the Bicep compiler
> is what caught it. A longer prefix fails at deploy time.
> ⚠️ **`countryCode` sets data residency and cannot be changed afterwards.** Choose it
> deliberately.

### What ARM does *not* create — you must do this yourself

Everything *inside* the directory is tenant-scoped and outside ARM's reach. These four
steps are the **entire manual surface of a deployment**; everything else in this document
is scripted.

Do them in this order. Steps 1 and 2 come first because a redirect URI is matched
exactly — register the generated Static Web App hostname now and you will redo both the
app registration and the front end when the real domain arrives.

#### 1. Point the domain at the Static Web App *(your DNS provider)*

Add a `CNAME` for the hostname you intend to use, pointing at the deployment's
`staticWebAppHostname` output.

> ⚠️ **If your DNS is behind a proxy — Cloudflare's orange cloud, or equivalent — turn it
> off for this record.** Azure validates ownership and renews the certificate by resolving
> the name to the static web app over the public internet. A proxy answers with its own
> addresses, and the failure is not an error today: it is a certificate that silently fails
> to renew in about three months. Static Web Apps already provides a global CDN and a free
> auto-renewed certificate, so a proxy in front duplicates the one and endangers the other.

#### 2. Add the custom domain *(Azure portal)*

Static Web App → **Custom domains** → **+ Add** → **Custom domain on other DNS**. Add the
`TXT` record it asks for, and wait for the status to read **Ready** before continuing. The
certificate is issued automatically.

#### 3. Register the application *(Entra admin centre, external tenant)*

Sign in at `entra.microsoft.com` and switch directory to the external tenant.

- **App registrations → New registration**, accounts in this directory only.
- Platform **Single-page application**, redirect URI = `https://<your-domain>`.
- **Expose an API**: accept the default Application ID URI, add a scope.
- **API permissions**: add that scope from *My APIs*, then grant admin consent.

#### 4. Create the user flow and attach the app *(same place)*

**External Identities → User flows → New user flow**. Include **Email** among the
attributes returned, since the panel shows it to whoever approves the account. Then, inside
the flow, **Applications → Add application**.

#### Then feed two values back to the deployment

| Value | Where it goes |
| --- | --- |
| Application (client) ID | `panelOidcAudience` |
| Authority URL for the tenant | `panelOidcAuthority` |

> **Read the audience, do not derive it.** Sign in once, decode the access token, and use
> the `aud` claim verbatim. The verifier compares it literally, and a guess produces a 401
> that looks like a credentials problem and is not one.

These four steps are also precisely why moving to a new tenant is a **rebuild, not a
migration** — see §6. They are scriptable through Microsoft Graph, which is the obvious
next improvement; until that exists, this list is the whole of it.

---

## 5. The data tier is private by default

Cosmos DB and the storage account ship with `publicNetworkAccess = Disabled` and are
reachable only through private endpoints from inside the Container Apps environment.

The consequence, which you will hit within five minutes of development: you cannot query
Cosmos from your laptop. That is intended. Two ways forward:

- **Preferred** — never let a browser or a laptop touch the data tier directly. The API
  proxies what it needs to, using its managed identity. This is also why the sheet preview
  is streamed through our own endpoint rather than handed out as a SAS URL: an SVG can
  carry a `<script>`, and serving it from our origin lets us apply a content security
  policy.
- **When you genuinely need direct access** — redeploy with
  `-p dataPublicNetworkAccess=Enabled`, do the work, then set it back. The private
  endpoints are created either way, so nothing else changes.

**No keys anywhere.** Cosmos has `disableLocalAuth: true`, the storage account has
`allowSharedKeyAccess: false`, and the registry has the admin user disabled. Everything
authenticates with the managed identity. Cosmos keys in particular cannot be scoped down,
so a leaked one gives full access.

### A note for the MCAPS-style subscriptions

If you deploy into a Microsoft-sponsored subscription, you may have read that public
endpoints are forbidden. Checked against the actual policy set on 6 Aug 2026: the deny
initiative contains eleven policies and **none of them concerns `publicNetworkAccess`** —
it is covered by an *audit* initiative. You are therefore not blocked on day one, but
audit findings are still findings, and the posture above is the right one anyway.

---

## 6. Moving to a different subscription or tenant

This is designed for. No tenant id, subscription id, object id or email appears anywhere in
`infra/`.

**A different subscription** is a redeploy: point the script at the new one.

**A different tenant is a rebuild, not a migration.** Identities do not move. You will
recreate:

- the app registrations (their client ids change)
- the External ID user flows and the accounts inside them
- every managed identity — and therefore every role assignment, including the Cosmos
  data-plane ones that reference principal ids

The templates handle all of that automatically. What does not come along is the *contents*
of the old External ID directory: accounts must be created again. Plan for it rather than
discovering it.

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

The first request after an idle period pays a cold start, because `minReplicas` is zero.
That is the intended trade: no traffic, no bill.

---

## 8. Tearing it down

```powershell
az group delete -n rg-lanternina-dev-app --yes      # disposable
az group delete -n rg-lanternina-dev-core --yes
az group delete -n rg-lanternina-dev-data --yes     # ⚠️ households, and the directory
```

Deleting the data resource group deletes the External ID directory and every account in
it, along with the households in Cosmos. There is no undo.

---

## 9. Things that will bite you

Collected from doing this, not from documentation.

- **`az acr build` crashes on Windows** with `UnicodeEncodeError` while streaming build
  logs through the console's default encoding. The server-side build *succeeds* and pushes
  the image; only the local process dies, so any later step in your script is silently
  skipped. Use `--no-logs`, or set `$env:PYTHONUTF8 = '1'` first.
- **PowerShell eats `||` inside a JMESPath `--query`**, even between double quotes: the
  argument is truncated at the first `||`. Filter with `Select-String` instead.
- **Import the base image into your registry** (`az acr import`) rather than pulling from
  Docker Hub on every build, or you will meet the anonymous rate limit at the worst moment.
- **Keep the registry in the same region as the Container Apps environment.** Image pull
  time is a large part of cold start.
- **Log Analytics is the quiet cost driver**, not Cosmos. The template caps retention at 30
  days and daily ingestion at 1 GB. Raise it deliberately, not by accident.
