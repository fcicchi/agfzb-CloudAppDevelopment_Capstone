const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    if (params.state)
    {
        let dbListPromise = getMatchingStateRecords(cloudant, "dealerships", params.state);
        return dbListPromise;
    }
    else
    {
        let dbListPromise = getAllRecords(cloudant, "dealerships");
        return dbListPromise;
    }
}

function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true})            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
}

function getMatchingStateRecords(cloudant,dbname, state) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname, selector: { st: { "$eq" : state}}})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
}