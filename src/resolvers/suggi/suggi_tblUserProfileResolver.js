const suggi_tblUserProfile = require("../../models/suggi/suggi_tblUserProfile");

const suggi_tblUserProfileResolver = {
  Query: {
    suggi_users: async () => {
      try {
        const suggi_users = await suggi_tblUserProfile.find();
        return suggi_users;
      } catch (error) {
        throw new Error("User data not found");
      }
    },
    suggi_getUserDataById: async (parent, args) => {
      try {
        const userData = await suggi_tblUserProfile.findById(args._id);

        return userData;
      } catch (error) {
        throw new Error("User data not found");
      }
    },
    suggi_getReferralCounts: async () => {
      try {
        const result = await suggi_tblUserProfile.aggregate([
          {
            $match: { ReferralId: { $ne: "" } },
          },
          {
            $group: {
              _id: "$ReferralId",
              count: { $sum: 1 },
            },
          },
        ]);

        const formattedResults = result.map((item) => {
          return {
            ReferralId: item._id,
            count: item.count,
          };
        });
        return formattedResults;
      } catch (error) {
        console.error("Error:", error);
      }
    },
    suggi_pincodeWiseDownloads: async() => {
      try{
        const data = await suggi_tblUserProfile.aggregate([
          {
            $match: { ReferralId: { $ne: "" } },
          },
          {
            $lookup: {
                from: 'tblUserAddress',
                localField: 'AddressId',
                foreignField: '_id',
                as: 'Address'
            }
          },
          {
            $unwind: '$Address'
          },
          { 
            $group: {
              _id: "$_id",
              pincode: {$first:{ $first: "$Address.Address.Pincode" }}
            } 
          },
          {
            $group:{
              _id:"$pincode",
              pincode: {$first:"$pincode"},
              downloads: {$sum:1},
            }
          },
          {
            $project:{
              _id:0
            }
          }
        ])
        console.log(data)
        return data
      }
      catch(err){
        return err
      }
    }

  },
};

module.exports = suggi_tblUserProfileResolver;
