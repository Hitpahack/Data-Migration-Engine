const fs = require("fs");
const path = require("path");


// Suggi Schema files
//----------------------------------------------------------------------------------
const suggi_tblUserProfileSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblUserProfile.graphql"),
  "utf8"
);
const suggi_tblUserBankSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblUserBank.graphql"),
  "utf8"
);
const suggi_tblUserAddressSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblUserAddress.graphql"),
  "utf8"
);
const suggi_tblStateDistrictSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblStateDistrict.graphql"),
  "utf8"
);

const suggi_tblCommoditiesSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblCommodities.graphql"),
  "utf8"
);
const suggi_tblGovtSchemeActivitySchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblGovtSchemeActivity.graphql"),
  "utf8"
);
const suggi_tblLanguagesSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblLanguages.graphql"),
  "utf8"
);
const suggi_tblLikesDislikesSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblLikesDislikes.graphql"),
  "utf8"
);
const suggi_tblNewsActivitySchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblNewsActivity.graphql"),
  "utf8"
);
const suggi_tblUserChatSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblUserChat.graphql"),
  "utf8"
);

const suggi_tblSuggiSalesSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblSuggiSales.graphql"),
  "utf8"
);

const suggi_inventorySchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_inventory.graphql"),
  "utf8"
);

const suggi_tblPurchaseOrderSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblPurchaseOrder.graphql"),
  "utf8"
);

const suggi_tblStockTransferSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_tblStockTransfer.graphql"),
  "utf8"
);

const suggi_storeTargetSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_storeTarget.graphql"),
  "utf8"
);

const suggi_storeCostingSchemaFile = fs.readFileSync(
  path.join(__dirname,"suggi/", "suggi_storeCost.graphql"),
  "utf8"
);
//----------------------------------------------------------------------------------


// Siri Schema files
const siri_tblTransactionSchemaFile = fs.readFileSync(
  path.join(__dirname,"siri/", "siri_tblTransaction.graphql"),
  "utf8"
);

const siri_tblSalesSchemaFile = fs.readFileSync(
  path.join(__dirname,"siri/", "siri_tblSales.graphql"),
  "utf8"
);

const siri_tblInventorySchemaFile = fs.readFileSync(
  path.join(__dirname,"siri/", "siri_tblInventory.graphql"),
  "utf8"
);

const typeDefs = `
  ${suggi_tblUserProfileSchemaFile}
  ${suggi_tblUserBankSchemaFile}
  ${suggi_tblUserAddressSchemaFile}
  ${suggi_tblStateDistrictSchemaFile}
  ${suggi_tblCommoditiesSchemaFile}
  ${suggi_tblGovtSchemeActivitySchemaFile}
  ${suggi_tblLanguagesSchemaFile}
  ${suggi_tblLikesDislikesSchemaFile}
  ${suggi_tblNewsActivitySchemaFile}
  ${suggi_tblUserChatSchemaFile}
  ${suggi_tblSuggiSalesSchemaFile}
  ${suggi_inventorySchemaFile}
  ${siri_tblTransactionSchemaFile}
  ${suggi_tblPurchaseOrderSchemaFile}
  ${siri_tblSalesSchemaFile}
  ${siri_tblInventorySchemaFile}
  ${suggi_tblStockTransferSchemaFile}
  ${suggi_storeTargetSchemaFile}
  ${suggi_storeCostingSchemaFile}

`;

module.exports = typeDefs;
