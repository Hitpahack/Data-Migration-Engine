const suggi_storeTarget = require("../../models/suggi/suggi_storeTarget");
console.log("hitt")
const suggi_StoreTargetResolver = {
    Query: {
        suggi_StoreTarget: async () => {
            return await suggi_storeTarget.aggregate([
                {
                    $match: {}
                }
            ]);
        },
    }
};

module.exports = suggi_StoreTargetResolver;