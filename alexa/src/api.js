// Main File for business logic

const {APP_VERSION, APP_STATES} = require('./consts');

function wrap(fnc) {
    return function inner() {
        // console.log("args:", arguments)
        // console.log("state:", this.handler.state)
        const that = this;
        try {
            fnc(that, arguments)
        } catch (err) {
            console.warn("[E] Caught err", err.message, err);
        }
    }
}

function handleNewSession(state) {
    return wrap(function(alexa) {
        console.log("Event:", JSON.stringify(alexa.event));
        const name = parseIntentNameFromRequest(alexa.event.request);
        console.log("NS_DBG:", state, name);
        Object.assign(alexa.attributes, updateState(alexa.attributes));
        alexa.emitWithState(name);
    })
}

const parseIntentNameFromRequest = (request) => {
    if (request.type === "IntentRequest") {
        return request.intent.name;
    }
    return request.type;
}

const generateInitialState = () => {
    const now = (new Date()).toISOString();
    const state = {sessions: 1, createdAt: now,
                   lastSession: now }
    return state;
}

const updateState = (prev) => {
    const now = (new Date()).toISOString();
    const {sessions} = prev;
    const nextState = {sessions: (sessions || 0) +1, lastSession: now }
    return nextState;
}

const toTitleCase = (str) => {
    return str.replace(/\w\S*/g,
        function(txt){
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
}

const strip = (str) => { return str.replace(/\s/g, "_") }

const stringEval = (str) => {
    if (!str || str == "NULL") {
        return null
    }
    return str;
}

function getAvailableCommands (med) {
    var text = "You can say: Hello, Goodbye";
    return text
}

module.exports = {
    wrap: wrap,
    handleNewSession: handleNewSession,
    parseIntentNameFromRequest: parseIntentNameFromRequest,
    stringEval: stringEval,
    toTitleCase: toTitleCase,
    getAvailableCommands: getAvailableCommands,
    generateInitialState: generateInitialState,
    updateState: updateState
}