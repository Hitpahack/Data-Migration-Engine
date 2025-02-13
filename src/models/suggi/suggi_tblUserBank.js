const mongoose = require("mongoose");

const tblUserBankDetails = new mongoose.Schema({
  _id: { type: mongoose.Schema.Types.ObjectId },
  Name: String,
  BankName: String,
  AccountNumber: String,
  IFSCCode: String,
  PaymentDuration: String,
  AccImageId: String,
  Status: String,
  CreatedBy: String,
  CreatedFrom: String,
  Default: Boolean,
});

const tblUserBankSchema = new mongoose.Schema({
  _id: { type: mongoose.Schema.Types.ObjectId },
  BankDetails: [tblUserBankDetails],
},{collection:"tblUserBank"});

const tblUserBank = mongoose.model("tblUserBank", tblUserBankSchema);

module.exports = tblUserBank;
