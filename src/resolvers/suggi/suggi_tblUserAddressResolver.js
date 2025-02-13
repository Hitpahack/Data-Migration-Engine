const suggi_tblUserAddress = require("../../models/suggi/suggi_tblUserAddress");

const suggi_userAddressResolvers = {
  Query: {
    suggi_getUserAddressByID : async (_, { _id }) => {
      return await suggi_tblUserAddress.findById(_id);
    },
    
  },
};

module.exports = suggi_userAddressResolvers;
