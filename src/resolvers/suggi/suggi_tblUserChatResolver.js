const suggi_tblUserChat = require("../../models/suggi/suggi_tblUserChat");

const suggi_tblUserChatResolver = {
  Query: {
    suggi_getChatById: async (_, {id}) =>  await suggi_tblUserChat.findById(id),

    suggi_totalChatActivity: async () => {
        try {
          const data = await suggi_tblUserChat
            .aggregate([
              {
                $match: { user_id: { $ne: "" } },
              },
              {
                $project: {
                    activityCount: { $size: "$chat_data" },
                    UserId: { $toObjectId: "$user_id"},
                    _id:0
                },
              },
              // {
              //   $lookup: {
              //       from: 'tblUserProfile',
              //       localField: "UserId",
              //       foreignField: '_id',
              //       as: 'User'
              //   }
              // },
              // {
              //   $unwind:"$User"
              // },
              {
                $group:{
                    _id:"$UserId",
                    UserId: {$first: "$UserId"},
                    activityCount: {$sum:"$activityCount"}
                }
              }
            ])
            .exec();
          console.log(data)
          return data;
        } catch (err) {
          console.log(err);
          return err;
        }
      },
      suggi_totalChatActivityPin: async () => {
        try {
          const data = await suggi_tblUserChat
            .aggregate([
              {
                $match: { user_id: { $ne: "" } },
              },
              {
                $project: {
                    activityCount: { $size: "$chat_data" },
                    UserId: { $toObjectId: "$user_id"},
                    _id:0
                },
              },
              {
                $lookup: {
                    from: 'tblUserProfile',
                    localField: "UserId",
                    foreignField: '_id',
                    as: 'User'
                }
              },
              {
                $unwind:"$User"
              },
              {
                $lookup: {
                    from: 'tblUserAddress',
                    localField: 'User.AddressId',
                    foreignField: '_id',
                    as: 'Address'
                }
              },
              {
                $unwind: '$Address'
              },
              { 
                $group: {
                  _id: "$UserId",
                  pincode: {$first:{ $first: "$Address.Address.Pincode" }},
                  activityCount: {$sum:"$activityCount"}
                } 
              },
              {
                $group:{
                  _id:"$pincode",
                  pincode: {$first:"$pincode"},
                  activityCount: {$sum:"$activityCount"},
                }
              },
              {
                $project:{
                  _id:0
                }
              }
            ])
            .exec();
          console.log(data)
          return data;
        } catch (err) {
          console.log(err);
          return err;
        }
      },

      suggi_totalChatActivityDist: async () => {
        try {
          const data = await suggi_tblUserChat
            .aggregate([
              {
                $match: { user_id: { $ne: "" } },
              },
              {
                $project: {
                    activityCount: { $size: "$chat_data" },
                    UserId: { $toObjectId: "$user_id"},
                    _id:0
                },
              },
              {
                $lookup: {
                    from: 'tblUserProfile',
                    localField: "UserId",
                    foreignField: '_id',
                    as: 'User'
                }
              },
              {
                $unwind:"$User"
              },
              {
                $lookup: {
                    from: 'tblUserAddress',
                    localField: 'User.AddressId',
                    foreignField: '_id',
                    as: 'Address'
                }
              },
              {
                $unwind: '$Address'
              },
              { 
                $group: {
                  _id: "$UserId",
                  district: {$first:{ $first: "$Address.Address.District" }},
                  activityCount: {$sum:"$activityCount"}
                } 
              },
              {
                $group:{
                  _id:"$district",
                  district: {$first:"$district"},
                  activityCount: {$sum:"$activityCount"},
                }
              },
              {
                $project:{
                  _id:0
                }
              }
            ])
            .exec();
          console.log(data)
          return data;
        } catch (err) {
          console.log(err);
          return err;
        }
      },
  },
};

module.exports = suggi_tblUserChatResolver;
