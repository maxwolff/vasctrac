var expect = require('chai').expect;
var index = require('../src/index');
var config = require('../src/config');

const context = require('aws-lambda-mock-context');
const ctx = context();

/*
    NOTE: Need to manually clear STATE from DynamoDB to Test
 */

describe("Testing a session with NEW_USER", function() {
    var speechResponse = null
    var speechError = null

    before(function(done){
        index.handler({
            "session": {
                "sessionId": "SessionId.154291c5-a13f-4e7a-ab5a-2342534adfeba",
                "application": {
                    "applicationId": config.AWS_APP_ID
            },
            "attributes": {
                "STATE": null,
                "sessions": null,
                "createdAt": null,
                "lastSession": null,
            },
            "user": {
                "userId": config.AWS_USER_ID
            },
            "new": true
            },
            "request": {
                "type": "IntentRequest",
                "requestId": "EdwRequestId.474c15c8-14d2-4a77-a4ce-154291c5",
                "timestamp": "2016-07-05T22:02:01Z",
                "intent": {
                    "name": "AboutIntent",
                    "slots": { }
                },
                "locale": "en-US"
            },
            "version": "1.0"
        }, ctx)

        ctx.launchTimer();

        ctx.Promise
            .then(resp => { speechResponse = resp; done(); })
            .catch(err => { speechError = err; done(); })
    })

    describe("The response is structurally correct for Alexa Speech Services", function() {
        it('should not have errored',function() {
            expect(speechError).to.be.null
        })

        it('should have a version', function() {
            expect(speechResponse.version).not.to.be.null
        })

        it('should have a speechlet response', function() {
            expect(speechResponse.response).not.to.be.null
        })

        it("should have a spoken response", () => {
            expect(speechResponse.response.outputSpeech).not.to.be.null
            console.log(speechResponse.response.outputSpeech.ssml)
            console.log(speechResponse.sessionAttributes)
        })

        it("should end the alexa session", function() {
            expect(speechResponse.response.shouldEndSession).not.to.be.null
            expect(speechResponse.response.shouldEndSession).to.be.true
        })
    })
})