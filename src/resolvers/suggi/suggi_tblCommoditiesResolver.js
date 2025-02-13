const suggi_tblCommodities = require("../../models/suggi/suggi_tblCommodities");

const suggi_commoditiesResolvers = {
  Query: {
    suggi_suggi_getAllCommodities: async (_, { _id }) => {
      return await suggi_tblCommodities.findById(_id);
    },
    suggi_getAllCommodities: async () => {
      return await suggi_tblCommodities.find();
    },
  },
};

module.exports = suggi_commoditiesResolvers;
