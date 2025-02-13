const suggi_tblStateDistrict = require("../../models/suggi/suggi_tblStateDistrict");

const suggi_stateDistrictResolvers = {
  Query: {
    suggi_getStateDataByID : async (_,  {id} ) => {
      console.log(id)
      return await suggi_tblStateDistrict.findById(id);
    },
    
  },
};

module.exports = suggi_stateDistrictResolvers;
