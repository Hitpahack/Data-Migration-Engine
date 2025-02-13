
// Suggi Resolver exports
// --------------------------------------------------------------------------------------------------------------
const suggi_tblUserProfileResolver = require("./suggi/suggi_tblUserProfileResolver");
const suggi_tblUserBankResolver = require("./suggi/suggi_tblUserBankResolver");
const suggi_tblUserAddressResolver = require("./suggi/suggi_tblUserAddressResolver");
const suggi_tblStateDistrictResolver = require("./suggi/suggi_tblStateDistrictResolver");
const suggi_tblCommoditiesResolver = require("./suggi/suggi_tblCommoditiesResolver");
const suggi_tblGovtSchemeActivityResolver = require("./suggi/suggi_tblGovtSchemeActivityResolver");
const suggi_tblLanguagesResolver = require("./suggi/suggi_tblLanguagesResolver");
const suggi_tblLikesDislikesResolver = require("./suggi/suggi_tblLikesDislikesResolver");
const suggi_tblNewsActivityResolver = require("./suggi/suggi_tblNewsActivityResolver");
const suggi_tblUserChatResolver = require("./suggi/suggi_tblUserChatResolver");
const suggi_tblSuggiSalesResolver = require("./suggi/suggi_tblSuggiSalesResolver");
const suggi_tblStockProductResolver = require("./suggi/suggi_tblStockProductResolver");
const suggi_tblPOResolver = require("./suggi/suggi_tblPurchaseOrderResolver");
const suggi_tblStockTransferResolver = require("./suggi/suggi_tblStockTransferResolver");
const suggi_storeTargetResolver = require("./suggi/suggi_storeTargetResolver");
const suggi_storeCostingResolver = require("./suggi/suggi_storeCostingResolver");


//----------------------------------------------------------------------------------------------------------------


//Siri Resolver exports
const siri_tblTransactionResolvers = require("./siri/siri_tblTransactionResolver");
const siri_tblSalesResolver = require("./siri/siri_tblSalesResolver");
const siri_tblInventoryResolver = require("./siri/siri_tblInventoryResolver");



module.exports = {
  suggi_tblUserProfileResolver,
  suggi_tblUserBankResolver,
  suggi_tblUserAddressResolver,
  suggi_tblStateDistrictResolver,
  suggi_tblCommoditiesResolver,
  suggi_tblGovtSchemeActivityResolver,
  suggi_tblLanguagesResolver,
  suggi_tblLikesDislikesResolver,
  suggi_tblNewsActivityResolver,
  suggi_tblUserChatResolver,
  suggi_tblSuggiSalesResolver,
  suggi_tblStockProductResolver,
  siri_tblTransactionResolvers,
  suggi_tblPOResolver,
  siri_tblSalesResolver,
  siri_tblInventoryResolver,
  suggi_tblStockTransferResolver,
  suggi_storeTargetResolver,
  suggi_storeCostingResolver
};
