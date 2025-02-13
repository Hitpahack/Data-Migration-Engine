const mongoose = require('mongoose');

const storeCostSchema = new mongoose.Schema({
  Store:String,
  Month:String,
  Year:String,
  Date:Date,
  Store_Cost:Number,
  Daily_Store_Cost:Number,
},{ collection: "Store_Costing" });

const StoreCost = mongoose.model('Store_Costing', storeCostSchema);

module.exports = StoreCost;
