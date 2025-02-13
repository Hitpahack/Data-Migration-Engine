const mongoose = require('mongoose');
 const userSchema = {
    _id: mongoose.Schema.Types.ObjectId,
    Category: String,
    CropName: String,
    Quantity: Number,
    Unit: String,
    Soot: Number,
    Price: Number,
    Grade: String,
    createdBy: String,
    Payment: Boolean,
    ProductImageId: String,
    Miscellaneous: [String],
    HamaliDeduct: Number,
    LivesDeduct: Number,
    TransportationCharges: Number,
    WeighBridgeExpense: Number,
    APMCCess: Number,
    EmptyGunnyBag: Number,
    TotalMiscCharges: Number,
    QCParameter: [String],
    ApplyQC: Boolean,
    createdOn: Date,
    UserId: String,
    Bags: Number,
    InvoiceId: String,
    userName: String
  };

  const billingTransactionSchema = {
    _id: mongoose.Schema.Types.ObjectId,
    InvoiceID: String,
    FarmerId: String,
    BankDetail: String,
    LoadId: [String],
    DistrictCenter: String,
    GrnDate: Date,
    GST: Boolean,
    GSTtype: String,
    Status: String,
    CreatedBy: String,
    CreatedAt: Date,
    LastUpdatedOn: Date,
    TraderInvoiceAvailable: String,
    TraderInvoiceDate: Date,
    TraderInvoiceId: String,
    TraderInvoiceImgId: String,
    InvoiceDate: Date,
    LastUpdatedBy: String,
    PaymentUpdatedOn: Date,
    NetPayable: Number,
    PaymentProductId: String,
    PaymentsList: [
      {
        Type: String,
        Amount: Number,
        Status: String,
        CreatedBy: String,
        CreatedOn: Date,
        ApprovedBy: String,
        ApprovedOn: Date,
        PaidBy: String,
        PaidOn: Date,
        PaymentMode: String,
        ReferenceNo: String,
        UpdatedBy: String,
        UpdatedOn: Date,
      },
    ],
  };

const inventorySchema = new mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    lotId:Number,
    userDetails: userSchema,
    billingTransaction: billingTransactionSchema,
    InventoryStatus:String,
    StockAmount:Number,
    ProcurredQty:Number,
    initialStock: Number,
    GodownID: String,
    GodownName: String,
    CreatedAt: Date
}, { collection: "siri_tblGodownInventory" });

const siri_tblGodownInventory = mongoose.model('siri_tblGodownInventory', inventorySchema);

module.exports = siri_tblGodownInventory
