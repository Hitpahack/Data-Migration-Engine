const suggi_tblGovtSchemeActivity = require("../../models/suggi/suggi_tblGovtSchemeActivity");
const mongoose = require("mongoose");

const suggi_govtSchemeActivityResolvers = {
  Query: {
    suggi_getGovtSchemeActivityById: async (_, { _id }) => {
      return await suggi_tblGovtSchemeActivity.findById(_id);
    },
    suggi_getAllGovtSchemeActivities: async () => {
      return await suggi_tblGovtSchemeActivity.find();
    },
    suggi_getNumberOfGovtSchemeActivitiesByUserId: async (parents, { UserId }) => {
      try {
        // const test_data = suggi_tblGovtSchemeActivity.find({}).select(UserId: new mongoose.Types.ObjectId(UserId))
        // console.log(test_data)
        console.log(UserId)
        const data = await suggi_tblGovtSchemeActivity
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
        console.log(data);
        return data[0].activityCount;
      } catch (err) {
        console.log(err);
        return err;
      }
    },
    suggi_totalGovSchemeActivity: async () => {
      try{
        const data = await suggi_tblGovtSchemeActivity.aggregate([
          {
            $project: {
              activityCount: {$size: "$Activity" },
              UserId:1 
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
          // {
          //   $project:{
          //     Name : {
          //       $concat: [ "$User.FirstName", " ", "$User.LastName" ]
          //     },
          //     UserId:1,
          //     activityCount:1
          //   }
          // }
        ])
        .exec();
        // console.log(data)
        return data
      }
      catch(err){
        console.log(err)
        return err
      }
    },
    suggi_totalGovSchemeActivityPin: async () => {
      try{
        const data = await suggi_tblGovtSchemeActivity.aggregate([
          {
            $project: {
              activityCount: {$size: "$Activity" },
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
        .exec();
        // console.log(data)
        return data
      }
      catch(err){
        console.log(err)
        return err
      }
    },

    suggi_totalGovSchemeActivityDist: async () => {
      try{
        // const suggi_users = await suggi_tblGovtSchemeActivity.find({}).populate({
        //   path: 'UserId',
        //   populate: {
        //     path: 'AddressId',
        //     model: 'tblUserAddress'
        //   }
        // })
        // const groupedsuggi_users = {}
        // suggi_users.forEach(user => {
        //   try{
        //     const District = user.UserId.AddressId.Address[0].District
        //     if (!groupedsuggi_users[District]) {
        //       groupedsuggi_users[District] = {"Sum":0}
        //     }
        //     groupedsuggi_users[District].Sum+=user.Activity.length
        //   }
        //   catch{}
        // });
        // const result = []
        // for (const [key, value] of Object.entries(groupedsuggi_users)) {
        //   result.push(
        //     {
        //       "district":key,
        //       "activityCount":value.Sum
        //     }
        //   )
        // }
        // return result
        
        const data = await suggi_tblGovtSchemeActivity.aggregate([
          {
            $project: {
              activityCount: {$size: "$Activity" },
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
        .exec();
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

module.exports = suggi_govtSchemeActivityResolvers;
