const suggi_tblSuggiSales = require("../../models/suggi/suggi_tblsaleMaster");
console.log("hit")
const suggi_tblSuggiSalesResolvers = {
    Query: {
        suggi_getSaleWiseProfit: async () => {
            return await suggi_tblSuggiSales.aggregate([
                {
                    $match: {}
                }
            ]);
        },
    }
};

module.exports = suggi_tblSuggiSalesResolvers;