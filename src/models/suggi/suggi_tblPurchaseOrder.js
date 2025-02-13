const mongoose = require('mongoose');

const tblPurchaseOrderSchema = new mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    Id: Number,
    pono: String,
    podate: Date,
    store_ref: Number,
    status: String,
    remarks: String,
    type: String,
    createdby_ref: Number,
    createddatetime: Date,
    paymentstatus: String,
    products:[
        {
            po_product_mapping_mongo_id: mongoose.Schema.Types.ObjectId,
            po_product_mapping_id: Number,
            po_ref: Number,
            product_ref: Number,
            qty: Number,
            ftm_qty: Number,
            grndate: Date,
            rm_qty: Number,
            rsp: Number,
            supplier_product_mapping_mongo_id: mongoose.Schema.Types.ObjectId,
            posupplierid_ref: Number,
            poproduct_ref: Number,
            estimatedprice: Number,
            availableqty: Number,
            receivedqty: Number,
            GST: Number,
            eta: Date,
            combined_po_product_ref: String
        }
    ],
    supplier_details: {
        _id:  mongoose.Schema.Types.ObjectId,
        id: Number,
        name: String,
        gstnumber: String,
        isenabled: Boolean,
        address_ref: Number,
        picture_ref: Number,
        createddate: Date,
        category: String,
        msmeregistered: Boolean,
        msmenumber: String,
        tallycode: String
    }
},{collection:"tblpurchaseorder"});

const tblPurchaseOrder = mongoose.model('tblPurchaseOrderSchema', tblPurchaseOrderSchema);

module.exports = tblPurchaseOrder;
