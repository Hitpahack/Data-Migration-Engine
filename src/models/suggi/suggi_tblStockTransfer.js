const mongoose = require('mongoose');



const StCharges = {
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    others:Number,
    others:Number,
    transportcharges:Number,
    stock_transfer_receiptno:String,
    stock_transfer_receiptdate:Date
};
  
const StStore = {
    _id: mongoose.Schema.Types.ObjectId,
    id: Number,
    name:String    
};

const StStockTransferDetails = {
  _id: mongoose.Schema.Types.ObjectId,
  id: Number,
  stock_transfer_no:String,
  stock_transfer_date:Date,
  status:String,
  createddatetime:Date
};

const StProduct = {
  _id: mongoose.Schema.Types.ObjectId,
  id: Number,
  name:String,
  unit:String,
  qty:String,
  rate:Number,
  sellingprice:Number
};

const stocktransferSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  received_lot: Number,
  lotqty: Number,
  product: StProduct,
  stockTransferDetails:StStockTransferDetails,
  to_store:StStore, 
  from_store:StStore,
  charges:  StCharges,

},{collection:"tblStockTransfer"});

const tblSuggiStockTransfer = mongoose.model('tblStockTransfer',stocktransferSchema );

module.exports = tblSuggiStockTransfer;
