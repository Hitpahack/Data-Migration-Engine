const suggi_tblStockTransfer = require("../../models/suggi/suggi_tblStockTransfer");

const suggi_tblSuggiStockTransferResolvers = {
    Query: {
        suggi_getStockTransferDetails: async () => {
            const data=await suggi_tblStockTransfer.aggregate([
                {
                    $match: {}
                }
            ]);
            return data;
        },
    }
};

module.exports = suggi_tblSuggiStockTransferResolvers;