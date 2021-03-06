const Alexa = require('alexa-sdk');

const {APP_STATES, APP_VERSION} = require('../consts');
const {HELP_MESSAGES, LAUNCH_MESSAGES} = require("../helpers/messages");

const api = require("../api");

const BaseHandler = Alexa.CreateStateHandler(APP_STATES.MAIN, {
    // This will intercept any incoming intent or launch requests and route them to this handler.
    'NewSession': api.handleNewSession(APP_STATES.MAIN),
    "AboutIntent": api.wrap(function(alexa) {
        const cardTitle = "About";
        var speechOutput = "The Skill Developer, Zach Zeleznick, likes hiking, swimming, and lounging by the beach";
        alexa.emit(':tellWithCard', speechOutput, cardTitle, speechOutput);
    }),
    "MainIntent": api.wrap(function(alexa) {
        const cardTitle = "Main";
        const {Word} = alexa.event.request.intent.slots;
        const {value} = Word || {value: "Hello"}
        var speechOutput = `${value}`
        alexa.emit(':tellWithCard', speechOutput, cardTitle, speechOutput);
    }),
    "HowIsMyPadIntent": api.wrap(function(alexa) {
        const cardTitle = "How's my Pad?";
        const speechOutput = "Your ABI improved 10% this week based on your stride. You walked 5000 steps this week, which is 20% above your goal. Keep up the good work!"
        const card = speechOutput;
        const repromptText = "What else would you like to know?";
        alexa.emit(':askWithCard', speechOutput, repromptText, cardTitle, card);
    }),
    "WhatIsPadIntent": api.wrap(function(alexa) {
        const cardTitle = "What is Pad?";
        const speechOutput = "Peripheral artery disease (PAD) happens when plaque builds up in the wall of arteries in your legs, causing them to narrow, making walking painful."
        const card = speechOutput;
        const repromptText = "What else would you like to know?";
        alexa.emit(':askWithCard', speechOutput, repromptText, cardTitle, card);
    }),
    "ImprovePadIntent": api.wrap(function(alexa) {
        const cardTitle = "How Can I Improve?";
        const speechOutput = "Simple walking regimens and leg exercises can ease symptoms. A doctor can recommend a good treatment plan. Other important factors are improving diet, stopping smoking, and managing diabetes."
        const card = speechOutput;
        const repromptText = "What else would you like to know?";
        alexa.emit(':askWithCard', speechOutput, repromptText, cardTitle, card);
    }),
   "AMAZON.HelpIntent": function () {
        const {speech, card} = HELP_MESSAGES.BASE;
        const cardTitle = "Skill Help";
        const repromptText = "So how can I help?";
        this.emit(':askWithCard', speech, repromptText, cardTitle, card);
    },
    "AMAZON.StopIntent": function () {
        var speechOutput = "Goodbye";
        this.emit(':tell', speechOutput);
    },
    "AMAZON.CancelIntent": function () {
        var speechOutput = "Goodbye";
        this.emit(':tell', speechOutput);
    },
    "AMAZON.StartOverIntent": function() {
        var speechOutput = "Start over? ";
        speechOutput += "I'm having trouble understanding your intent."
        var repromptText = "If you'd like to verify your meds, "
        repromptText += "say 'verify meds'."
        this.emit(':ask', speechOutput, repromptText);
    },
    // Called when the user invokes the skill with the invocation name, but w/o command mapping to an intent.
    "LaunchRequest": function () {
        const {speech, card} = LAUNCH_MESSAGES.BASE;
        const cardTitle = "Skill Help";
        const repromptText = "So how can I help?";
        this.emit(':askWithCard', speech, repromptText, cardTitle, card);
    },
    /*
        1. The user says “exit”.
        2. The user does not respond or says something that does not match an intent defined in your voice interface while the device is listening for the user’s response.
        3. An error occurs.
     */
    'SessionEndedRequest': function () {
        console.log('base session ended! ' + this.event.request.reason);
        // Typically saved automatically, unless canceled or timed out
        this.emit(':saveState', true);
    },
    // Triggered when no intent matches Alexa request
    'Unhandled': function () {
        const helpText = "For instructions on what you can say, please say help me.";
        this.emit(':ask', helpText, helpText);
    }
});

module.exports = {
    BaseHandler: BaseHandler
}