const mongoose = require('mongoose');
require('dotenv').config(); 
const fs = require('fs');
const yaml = require('js-yaml');

const configs = readServerConfig()

// Database connection
mongoose
  .connect(configs['MONGO_URI'], {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log(configs['MONGO_URI']);
    console.log(`Db Connected`);
  })
  .catch(err => {
    console.log(err.message);
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

