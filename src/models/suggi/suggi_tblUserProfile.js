const mongoose = require("mongoose");

const tblUserProfileSchema = new mongoose.Schema({
  _id: { type: mongoose.Schema.Types.ObjectId },
  FirstName: String,
  LastName: String,
  Phone: {
    Primary: String,
  },
  email: {
    Primary: String,
    Secondary: String,
  },
  Languages: {
    Primary: String,
    Secondary: [String],
  },
  CreatedOn: Date,
  CommodityId: [
    { type: mongoose.Schema.Types.ObjectId, ref: "tblCommodities" },
  ],
  UserType: String,
  OTP: String,
  Role: String,
  AddressId: { type: mongoose.Schema.Types.ObjectId, ref: "tblUserAddress" },
  Gender: String,
  ReferralId: String,
  GCMID: String,
  ProfileImage: String,
  UserId: String,
  BankId: { type: mongoose.Schema.Types.ObjectId, ref: "tblUserBank" },
},{collection:"tblUserProfile"});

const tblUserProfile = mongoose.model("tblUserProfile", tblUserProfileSchema);

module.exports = tblUserProfile;
