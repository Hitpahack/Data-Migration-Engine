const mongoose = require("mongoose");

const tblNewsActivitySchema = new mongoose.Schema({
  UserId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "tblUserProfile"
  },
  Activity: [{
    NewsId: Number,
    TimeStamp: Date
  }],
  CreatedOn: Date
}, { collection: "tblNewsActivity" });

const tblNewsActivity = mongoose.model("tblNewsActivity", tblNewsActivitySchema);

module.exports = tblNewsActivity;
