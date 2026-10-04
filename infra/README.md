# Infrastructure Definitions

This directory contains Lanternina's Bicep entry point, parameter file, and infrastructure modules. The files describe deployment inputs. Their presence does not establish the current state of deployed resources.

The AI module connects an existing shared Foundry account. It creates Lanternina's project and runtime role assignments; it does not create the account or manage model deployments and quota. Set `aiResourceGroupName` and `aiExistingAccountName` for the target subscription. See [the deployment guide](../docs/DEPLOY.md#shared-foundry).