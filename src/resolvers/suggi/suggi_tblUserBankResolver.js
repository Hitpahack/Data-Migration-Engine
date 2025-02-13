const suggi_tblUserBank = require("../../models/suggi/suggi_tblUserBank");

const suggi_userBankResolvers = {
  Query: {
    suggi_getUserBankDetailsByID: async (_, { _id }) => {
      const data = await suggi_tblUserBank.findById(_id);
      console.log(data)
      return await suggi_tblUserBank.findById(_id);
    },
    
  },
};

module.exports = suggi_userBankResolvers;
