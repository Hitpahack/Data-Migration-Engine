const siri_tblTransaction = require("../../models/siri/siri_tblTransaction");

const siri_tblTransactionResolver = {
  Query: {
    siri_getAllTransactions: async () => {
      console.log("Hit")
      const transactionData = await siri_tblTransaction.find()
      console.log(transactionData.length);
      return transactionData;
    }
  }

};

module.exports = siri_tblTransactionResolver;
