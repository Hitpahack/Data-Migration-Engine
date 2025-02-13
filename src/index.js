const { ApolloServer } = require("@apollo/server");
const { startStandaloneServer } = require("@apollo/server/standalone");
require("dotenv").config();
require("./db-config");
const fs = require('fs');
const yaml = require('js-yaml');


const typeDefs = require("./schemas/schemas");
const {
  suggi_tblUserProfileResolver,
  suggi_tblUserBankResolver,
  suggi_tblUserAddressResolver,
  suggi_tblStateDistrictResolver,
  suggi_tblCommoditiesResolver,
  suggi_tblGovtSchemeActivityResolver,
  suggi_tblLanguagesResolver,
  suggi_tblLikesDislikesResolver,
  suggi_tblNewsActivityResolver,
  suggi_tblUserChatResolver,
  suggi_tblSuggiSalesResolver,
  suggi_tblStockProductResolver,
  siri_tblTransactionResolvers,
  suggi_tblPOResolver,
  siri_tblSalesResolver,
  siri_tblInventoryResolver,
  suggi_tblStockTransferResolver,
  suggi_storeTargetResolver,
  suggi_storeCostingResolver
} = require("./resolvers/resolvers");

const resolvers = [
  suggi_tblUserProfileResolver,
  suggi_tblUserBankResolver,
  suggi_tblUserAddressResolver,
  suggi_tblStateDistrictResolver,
  suggi_tblCommoditiesResolver,
  suggi_tblGovtSchemeActivityResolver,
  suggi_tblLanguagesResolver,
  suggi_tblLikesDislikesResolver,
  suggi_tblNewsActivityResolver,
  suggi_tblUserChatResolver,
  suggi_tblSuggiSalesResolver,
  suggi_tblStockProductResolver,
  siri_tblTransactionResolvers,
  suggi_tblPOResolver,
  siri_tblSalesResolver,
  siri_tblInventoryResolver,
  suggi_tblStockTransferResolver,
  suggi_storeTargetResolver,
  suggi_storeCostingResolver
];

//Apollo Server
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const configs = readServerConfig()

startStandaloneServer(server, {
  listen: { port: configs['PORT'] },
}).then(({ url }) => {
  if (configs['APP_MODE'] == "dev") {
    console.log(`Dev Server ready at ${url}`);
  } else if (configs['APP_MODE'] == "production") {
    console.log(`Production Server ready at ${url}`);
  } else{
    console.log("Server couldnt be started")
  }
});


function readServerConfig(){
  try {
    const yamlFilePath = '../server-config.yaml';
  
    const yamlFileContent = fs.readFileSync(yamlFilePath, 'utf8');
  
    const parsedData = yaml.load(yamlFileContent);
    console.log(parsedData)
    return parsedData;
  
  } catch (error) {
    console.error('Error reading or parsing the YAML file:', error);
  }
  
}