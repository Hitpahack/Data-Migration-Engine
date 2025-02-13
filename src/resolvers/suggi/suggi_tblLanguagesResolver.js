const suggi_tblLanguages = require("../../models/suggi/suggi_tblLanguages");

const suggi_languagesResolvers = {
  Query: {
    suggi_getLanguagesById: async (_, { _id }) => {
      return await suggi_tblLanguages.findById(_id);
    },
    suggi_getAllLanguages: async () => {
      return await suggi_tblLanguages.find();
    },
  },
};

module.exports = suggi_languagesResolvers;
