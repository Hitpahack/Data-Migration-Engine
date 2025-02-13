const suggi_tblNewsActivity = require("../../models/suggi/suggi_tblNewsActivity");
const mongoose = require("mongoose");
const suggi_newsActivityResolvers = {
  Query: {
    suggi_getNewsActivityById: async (_, { _id }) => {
      return await suggi_tblNewsActivity.findById(_id);
    },
    suggi_getAllNewsActivities: async () => {
      return await suggi_tblNewsActivity.find();
    },
    suggi_getNumberOfNewsActivitiesByUserId: async (_, { UserId }) => {
      try {
        const data = await suggi_tblNewsActivity
          .aggregate([
            {
              $match: {
                UserId: new mongoose.Types.ObjectId(UserId),
              },
            },
            {
              $project: {
                activityCount: { $size: "$Activity" },
              },
            },
          ])
          .exec();
        console.log(data)
        return data[0].activityCount;
      } catch (err) {
        console.log(err);
        return err;
      }
    },
    suggi_totalNewsActivity: async () => {
      try{
        const data = await suggi_tblNewsActivity.aggregate([
          {
            $project: {
              activityCount: { $size: "$Activity" },
              UserId:1
            },

          },
        ])
        // console.log(data)
        return data
      }
      catch(err){
        console.log(err)
        return err
      }
    },

    suggi_totalNewsActivityPin: async () => {
      try{
        const data = await suggi_tblNewsActivity.aggregate([
          {
            $project: {
              activityCount: { $size: "$Activity" },
              UserId:1
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
        // console.log(data)
        return data
      }
      catch(err){
        console.log(err)
        return err
      }
    },

    suggi_totalNewsActivityDist: async () => {
      try{
        const data = await suggi_tblNewsActivity.aggregate([
          {
            $project: {
              activityCount: { $size: "$Activity" },
              UserId:1
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
        // console.log(data)
        return data
      }
      catch(err){
        console.log(err)
        return err
      }
    }
  },
};

module.exports = suggi_newsActivityResolvers;
