const Alexa = require('alexa-sdk');

const {APP_STATES, SKILL_NAME} = require('../consts');
const api = require("../api");

// https://github.com/alexa/alexa-skills-kit-sdk-for-nodejs/issues/69
const NewHandler = Alexa.CreateStateHandler(APP_STATES.NEW_USER, {
    // This will intercept any incoming intent or launch requests and route them to this handler.
    'NewSession': function () {
        const name = api.parseIntentNameFromRequest(this.event.request);
        console.log("NS_DBG:", name);
        Object.assign(this.attributes, api.generateInitialState());
        this.handler.state = APP_STATES.MAIN;
        this.emitWithState(name);
    },
    'Unhandled': function () {
        const helpText = "For instructions on what you can say, please say help me.";
        this.handler.state = APP_STATES.MAIN;
        this.emit(':ask', helpText, helpText);
    }
});

const UndefinedHandler = Alexa.CreateStateHandler(APP_STATES.UNDEFINED, {
    'Unhandled': function () {
        const speechOutput = "Uh oh. We've run into a new error. Our developers are on the case!";
        console.warn("UndefinedHandler_DBG: state is", this.handler.state);
        this.handler.state = APP_STATES.MAIN;
        this.emit(':tell', speechOutput);
    }
});


module.exports = {
    NewHandler: NewHandler,
    UndefinedHandler: UndefinedHandler
}