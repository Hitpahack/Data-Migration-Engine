const mongoose = require('mongoose');

const addressSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    phone: String,
    alternatephone: String,
    email: String,
    street: String,
    pincode: Number,
    city: String,
    state_ref: Number,
    district_ref: Number,
    createddate: Date,
    village_ref: Number,
    address: String,
});

const userDetailsSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    name: String,
    username: String,
    password: String,
    role: String,
    address_ref: Number,
    createddate: Date,
    isalive: Boolean,
    store_ref: Number,
    address: addressSchema,
});

const storeDetailsSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    name: String,
    address_ref: Number,
    createddate: Date,
    invoiceformat: String,
    lastgeninvoiceno: Number,
    isenabled: Boolean,
    parent_ref: mongoose.Schema.Types.ObjectId,
    cashledger: String,
    upiledger: String,
    costcenter: String,
    territory_ref: Number,
    isStore: Boolean,
    vertical: String,
    territory: {
        name: String,
        zone: {
            name: String
        }
    },
    address: addressSchema,
});

const paymentSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    sale_ref: Number,
    cash: Number,
    card: Number,
    cardnumber: String,
    upi: Number,
    upinumber: String,
    paymentdate: Date,
    createddatetime: Date,
    cheque_ref: String,
});

const customerDetailsSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    name: String,
    phone: String,
    alternativephone: String,
    uniquecode: String,
    address_ref: Number,
    createddatetime: Date,
    GSTIN: String,
    src: Number,
    cust_type: String,
    iscouponapplicable: Boolean,
    address: addressSchema,
});

const lotDetailsSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    product_ref: Number,
    description: String,
    serialno: String,
    qadone: Boolean,
    qty: Number,
    dateofmanufacturing: Date,
    expirydate: Date,
    waranty_service: String,
    location: String,
    barcode: String,
    isbarcodegenerated: Boolean,
    status: String,
    receivedby_ref: Number,
    receiveddate: Date,
    invoice_ref: Number,
    store_ref: Number,
    rate: Number,
    discountmode: String,
    discount: Number,
    total: Number,
    sellingprice: Number,
    createddate: Date,
    gst: Number,
    productgroupbyguid: String,
    issellingpriceupdate: Boolean,
    mrp: Number,
    MiscCharge: Number,
    Margin: Number,
    baseunit: String,
    subqty: Number,
    subunit: String,
    soldqty: Number,
    lotnumber: String,
    hsn: String,
    defectiveqty: Number,
    saledefectiveqty: Number,
    combined_po_product_ref: String,
});

const purchaseProductDetailsSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    name: String,
    description: String,
    producttype_manufacture_ref: Number,
    isenabled: Boolean,
    picture_ref: mongoose.Schema.Types.ObjectId,
    createddate: Date,
    shortcode: String,
    inventory_track_mode: String,
    sku: String,
    createduser_ref: mongoose.Schema.Types.ObjectId,
    unit: String,
    subcategory_ref: Number,
    tradetype: String,
    technicalname: String,
    newsku: String,
    packingsize: String,
    uom: String,
    productsku: String,
    tatpercentage: Number,
    waranty_service: Number,
    hsn: Number,
    sub_category: {
        _id: mongoose.Schema.Types.ObjectId,
        id: Number,
        name: String,
        description: String,
        isenabled: Boolean,
        createddate: Date,
        shortcode: String,
        HSN_SAC: Number,
        deptcode: String,
        existingcategoryname: String,
        category_ref: Number,
    },
    manufacturer: {
        _id: mongoose.Schema.Types.ObjectId,
        id: Number,
        name: String,
        description: String,
        isenabled: Boolean,
        createdate: Date,
        shortcode: String,
    },
    category: {
        _id: mongoose.Schema.Types.ObjectId,
        id: Number,
        name: String,
        iscertificate: Boolean,
        createddatetime: Date,
        isenable: Boolean,
    },
});

const supplierDetailsSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    name: String,
    gstnumber: String,
    isenabled: Boolean,
    address_ref: Number,
    picture_ref: mongoose.Schema.Types.ObjectId,
    createddate: Date,
    category: String,
    msmeregistered: String,
    msmenumber: String,
    tallycode: String,
});

const productSchema = ({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    sale_ref: Number,
    product_ref: Number,
    discounttype: String,
    discount: Number,
    gst: Number,
    gstamount: Number,
    total: Number,
    soldqty: Number,
    sellingprice: Number,
    extradiscount: Number,
    servicecharge: Number,
    return_ref: mongoose.Schema.Types.ObjectId,
    isreturn: Boolean,
    storeTargetPerProduct: Number,
    _stock_product_ref: mongoose.Schema.Types.ObjectId,
    purchaseProductDetails: purchaseProductDetailsSchema,
    lotDetails: lotDetailsSchema,
    supplierDetails: supplierDetailsSchema,
});

const SuggiSalesMasterSchema = new mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    remarks: String,
    invoiceno: String,
    invoicedate: Date,
    grosstotal: Number,
    discounttype: String,
    discount: Number,
    gst: Number,
    total: Number,
    salestype: String,
    createddate: Date,
    SpecialDiscountAmount: Number,
    servicecharges: Number,
    couponcode: String,
    payment: paymentSchema,
    customerDetails: customerDetailsSchema,
    storeDetails: storeDetailsSchema,
    userDetails: userDetailsSchema,
    storeCost: Number,
    product: [productSchema],
    totalSoldQty: Number,
}, { collection: "tblsaleMaster" });

const SuggiSalesMaster = mongoose.model('tblsaleMaster', SuggiSalesMasterSchema);

module.exports = SuggiSalesMaster;
