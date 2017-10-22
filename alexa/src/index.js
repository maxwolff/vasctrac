const Alexa = require('alexa-sdk');
const AWS = require('aws-sdk');

const config = require("./config");
const {NewHandler, UndefinedHandler} = require("./handlers/_New");
const BaseHandler = require("./handlers/Base").BaseHandler;

AWS.config.update({region:'us-east-1'});
var dd = new AWS.DynamoDB();

exports.handler = function (event, context) {
    var alexa = Alexa.handler(event, context);
    alexa.appId = config.AWS_APP_ID;
    //  alexa.dynamoDBTableName = "Alexa-Padpiper";
    // required to save between asks!
    alexa.saveBeforeResponse = true;
    alexa.registerHandlers(NewHandler, UndefinedHandler, BaseHandler);
    alexa.execute();
};
