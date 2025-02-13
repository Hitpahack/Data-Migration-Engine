const mongoose = require('mongoose');

const productSchema = {
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
  isreturn: String,
  _stock_product_ref: mongoose.Schema.Types.ObjectId,
};

const paymentSchema = {
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
  cheque_ref: mongoose.Schema.Types.ObjectId,
};

const saleSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  id: Number,
  customer_ref: Number,
  store_ref: Number,
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
  saleby_ref: Number,
  SpecialDiscountAmount: Number,
  servicecharges: Number,
  couponcode: String,
  product: [productSchema],
  payment: paymentSchema,
  _customer_ref: mongoose.Schema.Types.ObjectId,
  _saleby_ref: mongoose.Schema.Types.ObjectId,
  _store_ref: mongoose.Schema.Types.ObjectId,
  storeCost: Number,
},{collection:"tblsale"});

const tblSuggiSales = mongoose.model('tblsale', saleSchema);

module.exports = tblSuggiSales;
