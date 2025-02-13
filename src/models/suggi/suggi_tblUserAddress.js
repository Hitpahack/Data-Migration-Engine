const mongoose = require("mongoose");

const addressDetails = new mongoose.Schema({
  _id: { type: mongoose.Schema.Types.ObjectId },
  Street: String,
  Locality: String,
  City: String,
  Block: String,
  Region: String,
  Division: String,
  District: String,
  State: String,
  Country: String,
  Pincode: String,
  Status: String,
  CreatedOn: Date,
});

const tblUserAddressSchema = new mongoose.Schema({
  _id: { type: mongoose.Schema.Types.ObjectId },
  Address: [addressDetails],
  CreatedOn: Date,
},{collection:"tblUserAddress"});

const tblUserAddress = mongoose.model("tblUserAddress", tblUserAddressSchema);

module.exports = tblUserAddress;
