const suggi_storeCost = require("../../models/suggi/suggi_storeCosting");
console.log("hit store cost")
const suggi_StoreCostResolver = {
    Query: {
        suggi_StoreCost: async () => {
            return await suggi_storeCost.aggregate([
                {
                    $match: {}
                }
            ]);
        },
    }
};

module.exports = suggi_StoreCostResolver;