const mongoose = require("mongoose");

const tblLikesDislikesSchema = new mongoose.Schema({
  UserId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "tblUserProfile"
  },
  Category: String,
  CategoryId: Number,
  Likes: Boolean,
  CreatedOn: Date
}, { collection: "tblLikesDisLikes" });

const tblLikesDislikes = mongoose.model("tblLikesDislikes", tblLikesDislikesSchema);

module.exports = tblLikesDislikes;
