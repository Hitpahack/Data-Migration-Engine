const mongoose = require('mongoose');

const tblUserChatSchema = new mongoose.Schema({
  _id : { type: mongoose.Schema.Types.ObjectId},
  user_id: { type: mongoose.Schema.Types.ObjectId, ref: "tblUserProfile" },
  date: Date,
  chat_data: [{
    message_id: String,
    message_type: String,
    time: Date,
    message_content: String,
    duration: String,
    response_audio: String,
    response_message: String,
    response_time: Date
  }]
  
},{collection:"tblUserChat"});

const tblUserChat = mongoose.model('tblUserChat', tblUserChatSchema);

module.exports = tblUserChat;
