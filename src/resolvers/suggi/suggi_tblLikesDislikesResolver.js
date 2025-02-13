const suggi_tblLikesDislikes = require("../../models/suggi/suggi_tblLikesDislikes");

const suggi_likesDislikesResolvers = {
  Query: {
    suggi_getLikesDislikesById: async (_, { _id }) => {
      return await suggi_tblLikesDislikes.findById(_id);
    },
    suggi_getAllLikesDislikes: async () => {
      return await suggi_tblLikesDislikes.find();
    },
  },
};

module.exports = suggi_likesDislikesResolvers;
