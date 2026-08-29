# The environment a research run needs. Read from the deployed API on 29 August 2026, so a
# run here calls exactly what the house calls. Sourced with `. .\research\env.ps1`.
$env:AZURE_CONFIG_DIR = "C:\code\lanternina\.azure"
$env:LANTERNINA_FOUNDRY_ENDPOINT = "https://ai-lanternina-dev-ssveb.services.ai.azure.com/api/projects/lanternina-dev"
$env:LANTERNINA_FOUNDRY_DEPLOYMENT = "gpt-5.6-sol-2026-07-09"
$env:LANTERNINA_FOUNDRY_FRONTIER_DEPLOYMENTS = "gpt-5.6-sol-2026-07-09,gpt-5.6-terra-2026-07-09,gpt-5.6-luna-2026-07-09"
$env:LANTERNINA_FOUNDRY_IMAGE_DEPLOYMENT = "gpt-image-2-2026-04-21"
$env:LANTERNINA_FOUNDRY_ACCOUNT_ENDPOINT = "https://ai-lanternina-dev-ssveb.cognitiveservices.azure.com"
$env:LANTERNINA_CONTENT_SAFETY_ENDPOINT = "https://ai-lanternina-dev-ssveb.cognitiveservices.azure.com/"
$env:PYTHONWARNINGS = "ignore"
