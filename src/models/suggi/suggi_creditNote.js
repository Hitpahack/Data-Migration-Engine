const mongoose = require('mongoose');

const creditNoteSchema = new mongoose.Schema({
  id: Number,
  creditnotenumber: String,
  creditnotedate: Date,
  remarks: String,
  total: Number,
  creditnotestatus: String,
  supplier_ref: Number,
  picture_ref: Number,
  isapproved: Boolean,
  store_ref: Number,
  createddatetime: Date,
  redeemedamount: Number,
},{ collection: "tblcreditnote" });

const CreditNote = mongoose.model('tblcreditnote', creditNoteSchema);

module.exports = CreditNote;
