const suggi_tblStockProduct = require("../../models/suggi/suggi_tblStockProduct")

const suggi_tblStockProductResolvers = {
    Query: {
        suggi_getInventory : async ()=>{
          const result = await suggi_tblStockProduct.aggregate([
        {
            $lookup: {
                  from: "tblsupplier",
                  localField: "invoice.supplier_ref",
                  foreignField: "id",
                  as: "supplier",
            },
        },
        {
            $unwind: {
                path:"$supplier",
                preserveNullAndEmptyArrays: true
            }
        },
        {
            $lookup: {
                from: "tblproduct",
                localField: "product_ref",
                foreignField: "id",
                as: "productDetails",
            },
        },
        {
            $unwind: {
                path:"$productDetails",
                preserveNullAndEmptyArrays: true
            }
        },
        {
            $lookup: {
                from: "tblstore",
                localField: "store_ref",
                foreignField: "id",
                as: "storeDetails",
            },
        },
        {
            $unwind: {
                path:"$storeDetails",
                preserveNullAndEmptyArrays: true
            }
        },
        
          ])
          console.log(result)
          return result
        }
    },
  };
  
  module.exports = suggi_tblStockProductResolvers;