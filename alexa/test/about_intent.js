var expect = require('chai').expect;
var index = require('../src/index');
var config = require('../src/config');

const context = require('aws-lambda-mock-context');
const ctx = context();

describe("Testing a session with AboutIntent", function() {
    var speechResponse = null
    var speechError = null

    before(function(done){
        index.handler({
            "session": {
                "new": true,
                "sessionId": "SessionId.3aee2288-1141-46ca-95f2-b0028586cea5",
                "application": {
                    "applicationId": config.AWS_APP_ID,
                    "attributes": {},
                    "user": {
                        "userId": config.AWS_USER_ID
                    }
                }
              },
              "request": {
                "type": "IntentRequest",
                "requestId": "EdwRequestId.67f7f400-f5e7-4a87-8363-709940320476",
                "intent": {
                  "name": "AboutIntent",
                  "slots": {}
                },
                "locale": "en-US",
                "timestamp": "2017-10-22T19:41:06Z"
              },
              "context": {
                "AudioPlayer": {
                  "playerActivity": "IDLE"
                },
                "System": {
                  "application": {
                    "applicationId": config.AWS_APP_ID
                  },
                  "user": {
                    "userId": config.AWS_USER_ID
                  },
                  "device": {
                    "supportedInterfaces": {}
                  }
                }
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
        })

        it("should end the alexa session", function() {
            expect(speechResponse.response.shouldEndSession).not.to.be.null
            expect(speechResponse.response.shouldEndSession).to.be.true
        })
    })
})