const mongoose = require("mongoose");

const tblGovtSchemeActivitySchema = new mongoose.Schema({
  UserId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "tblUserProfile"
  },
  Activity: [{
    GovtSchemeId: Number,
    TimeStamp: Date
  }],
  CreatedOn: Date
}, { collection: "tblGovtSchemeActivity" });

const tblGovtSchemeActivity = mongoose.model("tblGovtSchemeActivity", tblGovtSchemeActivitySchema);

module.exports = tblGovtSchemeActivity;
