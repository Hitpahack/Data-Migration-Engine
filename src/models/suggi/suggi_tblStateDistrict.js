const mongoose = require('mongoose');

const DistrictDetailsSchema = new mongoose.Schema({
  name: String,
});

const tblStateDistrictSchema = new mongoose.Schema({
  State: String,
  Districts: [DistrictDetailsSchema],
  GST: String,
  StateCode: Number,
},{collection:"tblStateDistrict"});

const tblStateDistrict = mongoose.model('tblStateDistrict', tblStateDistrictSchema);

module.exports = tblStateDistrict;
