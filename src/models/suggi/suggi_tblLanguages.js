const mongoose = require("mongoose");

const tblLanguagesSchema = new mongoose.Schema({
  Languages: [String],
  CreatedAt: Date
}, { collection: "tblLanguages" });

const tblLanguages = mongoose.model("tblLanguages", tblLanguagesSchema);

module.exports = tblLanguages;
