# Letting a pipeline change Azure without giving it a secret

How `.github/workflows/api.yml` signs in to Azure. There is no password, no certificate and no service principal secret anywhere in this repository, in GitHub, or on a laptop — and nothing that expires and has to be renewed.

`docs/DEPLOY.md` §4b is the runbook: what exists today, what it may do, and how to remove it. This file is the method and the reasoning, so that the next one of these can be set up without rediscovering the three things that went wrong on 4 September 2026.

---

## 1. What it replaces

The ordinary way to let a build change cloud resources is to create a service principal with a secret and paste the secret into the CI system. Everything unpleasant about that follows from the secret being a bearer token: it works from anywhere, for anyone holding it, until somebody remembers to rotate it. It has to be stored, it leaks into logs by accident, and its expiry is a calendar problem nobody owns.

Workload identity federation removes the secret rather than protecting it. GitHub already knows which repository and which branch a job is running for, and it will say so in a signed token. Entra can be told to accept that statement as proof. What crosses the network is then a token that lives for minutes and is worthless anywhere else.

---

## 2. Why a user-assigned managed identity

Two kinds of principal can carry a federated credential: an **app registration** and a **user-assigned managed identity**. A **system-assigned** identity cannot — it has nowhere to register one and does not exist before the resource that hosts it, so the choice is only ever between the first two.

A user-assigned managed identity was chosen here, for four reasons that are about operations rather than security.

**It lives with the project.** A managed identity is an Azure resource in a resource group, beside the registry it pushes to. Delete the group and it goes, and its role assignments and federated credentials go with it. An app registration is a directory object: it outlives everything it governed, and old tenants fill up with orphaned principals nobody can connect to anything.

**Creating it needs no directory role.** `az identity create` is an ordinary resource write, so Owner on the subscription is enough. An app registration needs a role over the whole tenant. Measured on 4 September 2026: the identity, its credential and its three role assignments were all created with rights that were already held, and the Global Administrator elevation that had been taken for the purpose turned out to be unnecessary.

**It has nowhere to put a secret.** Neither kind needs one under federation, so on that day they are equal. But an app registration *can* have a client secret, and one day somebody in a hurry adds one to make a local script work, and the guarantee that there is nothing to leak quietly stops being true. A managed identity has no such field. The property is structural rather than promised.

**It is created the way everything else here is created.** This repository's rule is that things normally done by hand are done by hand — the Entra app registrations in §4 of the runbook are clicked through the portal on purpose. Nobody creates a managed identity by clicking, so that rule does not reach this.

What an app registration buys, and none of it is needed by a job that pushes an image: application permissions on Microsoft Graph, an exposed API scope, multi-tenancy, and interactive sign-in for a person.

---

## 3. What the trust actually is

There is no setting anywhere that says *trust GitHub*. No identity provider is registered, no enterprise application is created, no administrator consent is given. Nothing about the tenant changes.

The whole of it is one row on one identity:

```
issuer     https://token.actions.githubusercontent.com
subject    repo:<owner>@<owner_id>/<repo>@<repo_id>:ref:refs/heads/main
audiences  api://AzureADTokenExchange
```

**The anchor is the issuer, because it is an address Entra reads.** Entra fetches `/.well-known/openid-configuration` from it, follows `jwks_uri`, and verifies the token's signature against the public keys published there. Measured 4 September 2026: that endpoint served four RSA keys, all `RS256`. So the trust reduces to *whoever holds the private key for a key published at that HTTPS address*, which is GitHub and nobody else.

This is also why nothing has to be maintained. GitHub rotates those keys when it likes and republishes them; Entra reads them again. There is no certificate to renew and no date in anybody's calendar — which is the difference from a certificate uploaded by hand, and the reason this is less work rather than more.

Having checked the signature, Entra compares three claims against the row, and all three must match: `iss` that it came from that issuer, `aud` that the token was minted *for* Entra rather than for some other service that could then replay it, and `sub` which run it was.

**Nothing is trusted tenant-wide.** Measured on the same day across the three identities in this subscription:

```
id-lanternina-dev-runtime    federated credentials: 0
id-lanternina-dev-deploy     federated credentials: 0
id-lanternina-github         federated credentials: 1
```

A GitHub token opens nothing on the other two. Not because anybody forbade it — because no row permits it, and the default is none.

---

## 4. Where it says *my* pipeline and not somebody else's

In `sub`, and the reason it holds is that **the workflow cannot write it**. It is not a YAML field, not a variable and not an input to an action: GitHub's OIDC provider fills it in from where the run is actually happening. Somebody who copies this workflow into their own repository gets a token stating their coordinates, because that is the truth, and Entra refuses it.

It is a statement by a third party about a fact it knows, rather than a claim by the party being authenticated. That is the whole security argument, and everything else is detail.

**The numeric ids matter more than the names.** The subject carries both:

```
repo:faustinopalma@39453908/lanternina@1338031850:ref:refs/heads/main
     └── owner ──┘ └─ id ─┘ └─ repo ──┘ └─── id ───┘ └──── ref ────┘
```

GitHub never reuses account or repository ids, so the credential survives a rename and cannot be inherited by a later repository that happens to take the same name.

**The branch is pinned too.** A run on another branch presents `ref:refs/heads/<other>` and is refused; a pull request presents a subject ending in `:pull_request` and is refused. Neither is a policy written somewhere — they are simply different strings.

---

## 5. Setting one up

Five steps. Substitute your own names; the values shown are the ones this repository uses.

**1. The identity.**

```powershell
az identity create --name id-lanternina-github --resource-group rg-lanternina-dev-core --location swedencentral
```

Keep `clientId` and `principalId` from the output. The first goes to GitHub, the second is what role assignments are made against.

**2. The federated credential.** Register it with a subject you believe is right, then see §6 — you will probably have to correct it once, and that is the expected path rather than a mistake.

```powershell
az identity federated-credential create --name github-main `
  --identity-name id-lanternina-github --resource-group rg-lanternina-dev-core `
  --issuer "https://token.actions.githubusercontent.com" `
  --subject "repo:OWNER@OWNER_ID/REPO@REPO_ID:ref:refs/heads/main" `
  --audiences "api://AzureADTokenExchange"
```

**3. The roles, each on its own target.** Nothing at subscription or resource-group scope.

```powershell
az role assignment create --assignee-object-id <principalId> --assignee-principal-type ServicePrincipal `
  --role AcrPush --scope <registry resource id>
az role assignment create --assignee-object-id <principalId> --assignee-principal-type ServicePrincipal `
  --role Reader --scope <registry resource id>
az role assignment create --assignee-object-id <principalId> --assignee-principal-type ServicePrincipal `
  --role "Container Apps Contributor" --scope <container app resource id>
```

**4. Three repository variables**, not secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`. None of them is a credential — on their own they open nothing — and being readable in a log is what makes a failed sign-in diagnosable rather than mysterious.

**5. The workflow.** `id-token: write` is what lets the job ask GitHub for the assertion at all; without it the sign-in fails with no token rather than a rejected one.

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: azure/login@v3
    with:
      client-id: ${{ vars.AZURE_CLIENT_ID }}
      tenant-id: ${{ vars.AZURE_TENANT_ID }}
      subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

Measured end to end on 4 September 2026: sign-in, build, push, rollout and verification in **1 minute 35 seconds**.

---

## 6. The three things that went wrong, and what each cost

**The subject carries ids, not names, and this is the whole failure.** The first credential registered `repo:faustinopalma/lanternina:ref:refs/heads/main`, and the run ended at sign-in:

```
AADSTS700213: No matching federated identity record found for presented assertion subject
'repo:faustinopalma@39453908/lanternina@1338031850:ref:refs/heads/main'
```

⭐ **The error quotes the subject that actually arrived, in full.** So the method is not to write it correctly from a document that may be out of date: register something, run once, and read the real subject out of the refusal. That message is also the proof that this mechanism is a token exchange and nothing to do with IMDS — it is Entra reporting that it received an assertion and looked for a row matching it.

**`AcrPush` does not cover `az acr build`.** Its actions are exactly `Microsoft.ContainerRegistry/registries/pull/read` and `.../push/write`. `az acr build` queues a task on the registry and needs `scheduleRun`, which among built-in roles only `Contributor` carries. Keeping the familiar command would have meant an identity able to reconfigure or delete the registry in order to publish the same image, so the image is built on the runner with `docker build` instead. A side effect worth having: the build log appears in the run, rather than being suppressed by the `--no-logs` that works around the CLI's crash on non-ASCII output.

**`AcrPush` does not cover `az acr login` either.** It resolves the registry's login server through ARM, which is a control-plane read that the two data actions above do not include, so `Reader` on the registry was added alongside. ⚠️ Stated as the reason it was added rather than as a measurement: the working configuration was never tested without it. Removing it is the cheap experiment if this list is ever trimmed.

---

## 7. What this does not protect

The subject pins **a repository and a branch**. It does not pin a person. So the real question is who can push to that branch, and the answer is a GitHub setting rather than an Azure one.

Measured 4 September 2026 for this repository: one collaborator with push rights, `main` not protected, repository public. Public costs nothing here — anyone may fork it, and a fork presents a different subject — but the other two mean that anyone given push rights can reach production, and that a mistake goes out with nothing in the way.

**The way to tighten it, when this stops being a test environment**, is to move the subject from a branch to an environment: create a GitHub environment with required reviewers, declare `environment: production` in the job, and register a credential whose subject ends in `:environment:production`. An identity may hold several credentials at once, so both can exist during the change and there is no minute in which publishing is broken. It is deliberately not done here, because it would contradict the reason this pipeline exists — seeing production immediately after a push.

---

## 8. Reading it back, and removing it

Neither of these needs anything but the CLI, and both answer with the state rather than with what this file claims:

```powershell
az identity federated-credential list --identity-name id-lanternina-github -g rg-lanternina-dev-core -o table
az role assignment list --assignee <principalId> --all -o table
```

To take it all away, delete the identity: the assignments and the credentials go with it, and the workflow then fails at sign-in rather than doing something unexpected.

```powershell
az identity delete --name id-lanternina-github --resource-group rg-lanternina-dev-core
```

⚠️ Created by CLI and **not described in `infra/`**. A redeploy of `main.bicep` will not remove it, and will not recreate it either.

---

## 9. The same mechanism elsewhere

Nothing here is specific to GitHub. The issuer only has to be an OIDC provider publishing its keys at a URL, so GitLab, Terraform Cloud, Google and AWS work the same way with a different `issuer` and a different shape of `sub`.

It is also what AKS workload identity is made of: the cluster publishes an OIDC document, and a pod's service account is federated to a managed identity exactly as a repository is here. Worth knowing before meeting it under another name.
