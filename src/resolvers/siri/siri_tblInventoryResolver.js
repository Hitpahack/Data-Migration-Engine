const siri_Inventory = require("../../models/siri/siri_Inventory");

const siri_tblTransactionResolver = {
  Query: {
    siri_getInventory: async () => {
      console.log("Hit")
      const transactionData = await siri_Inventory.find()
      console.log(transactionData);
      return transactionData;
    }
  }
};

module.exports = siri_tblTransactionResolver;
