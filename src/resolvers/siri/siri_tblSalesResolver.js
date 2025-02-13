const siri_tblSales = require("../../models/siri/siri_tblSales");

const siri_tblTransactionResolver = {
  Query: {
    siri_getSales: async () => {
      console.log("Hit")
      const transactionData = await siri_tblSales.find()
      console.log(transactionData);
      return transactionData;
    }
  }

};

module.exports = siri_tblTransactionResolver;
