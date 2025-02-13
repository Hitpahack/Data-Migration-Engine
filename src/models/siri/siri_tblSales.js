const mongoose = require('mongoose');
const transportInformationSchema = {
    CompanyId: String,
    DriverName: String,
    DriverPhone: String,
    DriverLicence: String,
    VehicleNumber: String,
    Wheels: String,
    PaymentDate: Date,
    PaymentDone: Boolean,
    PaymentCompletedDate: Date,
    PaymentMode: String,
    UnloadedDate: Date,
    Approval: String,
    AdvanceAmount: Number,
    TransportAmount: Number,
    Total: Number,
    HaltingCharges: Number,
    InvoiceID: String,
};

const EwayBillSchema =
{
  _id: mongoose.Schema.Types.ObjectId,
  EwbNo: Number,
  EwbDt: Date,
  EwbValidTill: Date,
  EwayBillUrl: String,
  EwayBillRequestId: String,
  EwbUpdatedDate: Date,
  Status: String,
}

const consumerTransactionSchema = {
    InvoiceID: String,
    LoadId: String,
    BuyerId: String,
    DistrictCenter: String,
    CropName: String,
    UnLoadQuantity: Number,
    InvoiceQty: Number,
    Unit: String,
    PriceQuote: Number,
    POAmount: Number,
    PaymentDate: Date,
    PaymentDone: Boolean,
    PaymentCompletedDate: Date,
    SourceLoad: Boolean,
    LastUpdatedOn: Date,
    LastUpdatedBy: String,
    Status: String,
    InvoiceDate: Date,
    CreatedBy: String,
    CreatedAt: Date,
    ReferenceNo: String,
  };

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
    BuyerDeductions: Number,
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
    userName: String,
    UserOnboardingDate: Date
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


const users = {
    lotId:Number,
    userDetails: userSchema,
    billingTransaction: billingTransactionSchema,
    InventoryStatus:String,
    StockAmount:Number,
    ProcurredQty:Number,
  };
  
  const loadDetailsSchema = {
    users: [users],
    CropName: String,
    Quantity: Number,
    UnLoadQuantity: Number,
    FreeQty: Number,
    BiltyFreeQty: Number,
    Unit: String,
    Grade: String,
    GradeA: Number,
    WeighBridgeQty: Number,
    TotalProcurredQty: Number
  };

  
  
  


const saleSchema = new mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    BuyerId: String,
    PurchaseOrderId: String,
    LoadId: String,
    InvoiceID: String,
    TransportInformation:transportInformationSchema,
    HonorState: String,
    HonorDistrict: String,
    UserType: String,
    Status: String,
    TransactionType: String,
    LoadType: String,
    AssignType: String,
    createdBy: String,
    BiltyStatus: String,
    CreatedAt:Date,
    EwayBill:[EwayBillSchema],
    BuyerGRNImgId:String,
    BuyerGRNDeduction: Number,
    BuyerName:String,
    BuyerOnboardingDate: Date,
    CenterType: String,
    ConsumerTransaction:consumerTransactionSchema,
    LoadDetails:loadDetailsSchema,
    SellingPrice:Number
}, { collection: "siri_tblGodownSales" });

const siri_tblGodownSales = mongoose.model('siri_tblGodownSales', saleSchema);

module.exports = siri_tblGodownSales
