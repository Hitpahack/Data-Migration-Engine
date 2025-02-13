const mongoose = require('mongoose');

const storeTargetSchema = new mongoose.Schema({
  Store:String,
  TM:String,
  Category:String,
  Month:String,
  Year:String,
  Target:Number,
  Date:Date,
  Daily_Target:Number,
},{ collection: "Store_Target" });

const StoreTarget = mongoose.model('Store_Target', storeTargetSchema);

module.exports = StoreTarget;
