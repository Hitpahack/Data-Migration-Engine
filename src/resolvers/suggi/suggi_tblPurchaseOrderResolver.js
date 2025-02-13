const suggi_tblSuggiPO = require("../../models/suggi/suggi_tblPurchaseOrder.js");

const suggi_tblSuggiPOResolvers = {
    Query: {
        suggi_poDetails: async () => {
            const poDetails = await suggi_tblSuggiPO.aggregate([
                {
                    $lookup: {
                        from: "tblstore",
                        localField: "store_ref",
                        foreignField: "id",
                        as: "storedetails",
                    },
                },
                {
                    $unwind: {
                        path: "$storedetails",
                        preserveNullAndEmptyArrays: true
                    }
                },
                {
                    $unwind: "$products"
                },
                {
                    $lookup: {
                        from: "tblstockproduct",
                        localField: "products.combined_po_product_ref",
                        foreignField: "combined_po_product_ref",
                        as: "lotdetails",
                    },
                },
                {
                    $lookup: {
                        from: "tblproduct",
                        localField: "products.product_ref",
                        foreignField: "id",
                        as: "productdetails",
                    },
                },
                {
                    $unwind: {
                        path: "$productdetails",
                        preserveNullAndEmptyArrays: true
                    }
                },
                {
                    $group: {
                        _id: "$_id",
                        Id: { $first: "$Id" },
                        pono: { $first: "$pono" },
                        podate: { $first: "$podate" },
                        store_ref: { $first: "$store_ref" },
                        store_details: {$first:"$storedetails"},
                        status: { $first: "$status" },
                        remarks: { $first: "$remarks" },
                        type: { $first: "$type" },
                        createdby_ref: { $first: "$createdby_ref" },
                        createddatetime: { $first: "$createddatetime" },
                        paymentstatus: { $first: "$paymentstatus" },
                        totalOrderdqty: { $sum: "$products.availableqty"},
                        totalReceivedqty: { $sum: "$products.receivedqty"},
                        totalRequestedqty: {$sum: "$products.qty"},
                        products: {
                            $push: {
                                $mergeObjects: [
                                    "$products",
                                    {
                                        lotdetails: "$lotdetails"
                                    },
                                    {
                                        productData: "$productdetails"
                                    }

                                ],
                            },
                        },
                        supplier_details: { $first: "$supplier_details" },
                    },
                },
            ])
            return poDetails;
        },
        suggi_PO_Payment: async () => {
            const PO_Payment_Details = await suggi_tblSuggiPO.aggregate([
                {
                    $lookup: {
                        from: "tblpurchaseorder_payment_mapping",
                        localField: "Id",
                        foreignField: "po_ref",
                        as: "paymentDetails",
                    },
                },
                {
                    $unwind: {
                        path: "$paymentDetails",
                        preserveNullAndEmptyArrays: true
                    }

                },
                {
                    $group: {
                        _id: "$_id",
                        Id: { $first: "$Id" },
                        pono: { $first: "$pono" },
                        status: { $first: "$status" },
                        paymentstatus: { $first: "$paymentstatus" },
                        paymentDetails: { $push: "$paymentDetails" }
                    }
                }
            ])
            return PO_Payment_Details;
        }
    },
};

module.exports = suggi_tblSuggiPOResolvers;