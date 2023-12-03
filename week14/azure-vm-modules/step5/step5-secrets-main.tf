  data "azurerm_key_vault_secrets" "example" {
    key_vault_id = data.azurerm_key_vault.existing.id
  }
  
  data "azurerm_key_vault_secret" "example" {
    for_each     = toset(data.azurerm_key_vault_secrets.example.names)
    name         = each.key
    key_vault_id = data.azurerm_key_vault.existing.id
  }
  