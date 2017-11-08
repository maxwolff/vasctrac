## Introduction

Medbox is an Alexa Skill that helps users track and manage their medications. User can request refill information, their Rx list, directions, dosages, side effects, and manage claims.

### Purpose

Medbox was a 10-week future-facing project, exploring the capabilities and limitations of using Amazon Alexa to help Humana members manage their medications. The project goals were develop a working prototype, expanding on the work of the Hackathon Project created by [Zach Zeleznick](https://linkedin.com/in/zzeleznick) and [Ryan Ma](https://www.linkedin.com/in/ryan-ma), and prepare for an eventual pilot.

### User Interaction Model

[Flowchart](https://www.dropbox.com/s/2bsg5z2jjk7hnm3/Medbox%20by%20Humana.pdf?dl=0)


### Setup

1. Ensure node and npm is successfully installed and linked
2. Install required packages
    ```sh
    $ npm install
    ```
3. Copy `_dummyenv` to `_env` and replace AWS_APP_ID with your app id
    ```sh
    $ cp src/_dummyenv src/_env
    ```
4. Patch client libraries for custom test behavior -- see `diffs/README.md`
5. Run test suite to verify setup
    ```sh
    $ npm test
    ```

### Development

All source code for deployment lives inside of `src`. Environment variables are configured in `_env`
and should always be untracked in git. The interaction model and sample utterances live in `resources`,
but local changes to the model must be manually updated on the [Alexa Skills Dashboad](https://developer.amazon.com/edw/home.html).

### Testing

Integration tests live inside of `test` and can be run with `npm test` or via mocha. Sanity tests
should must be run via mocha with the filepath specified (e.g. `mocha sanity_tests/side-effects/exists.js`).
Code linting is powered by jshint and can be run via `npm run lint`.

### Deployment

Deployment is managed through [claudia.js](claudiajs.com), and some setup is required
to provision the account privileges.

```sh
# For first deployment
$ npm run deploy
```

```sh
# For subsequent deployments
$ npm run update
```

### Project Structure

    .
    ├── diffs/  [patch files for custom testing behavior]
    │   ├── alexa-sdk/
    │   │   └── alexa.js.diff
    │   ├── gulp-jshint/
    │   │   └── lint.js.diff
    │   ├── jshint/
    │   │   ├── jshint.js.diff
    │   │   └── options.js.diff
    │   ├── jshint-stylish/
    │   │   └── index.js.diff
    │   └── README.md
    ├── docs/
    │   └── example_test_results.txt
    ├── node_modules/ [485 entries]
    ├── resources/
    │   ├── slots/
    │   │   ├── AFFIRM.txt
    │   │   ├── COLORS.txt
    │   │   ├── CONDITIONS.txt
    │   │   ├── DRUGFIELDS.txt
    │   │   ├── MAYBE.txt
    │   │   ├── MEDTYPES.txt
    │   │   ├── REJECT.txt
    │   │   ├── SHAPES.txt
    │   │   └── TIMINGS.txt
    │   ├── Intent_Schema.txt
    │   └── Sample_Utterances.txt
    ├── sanity_tests/
    │   ├── refill/
    │   │   └── next_refill.js
    │   └── side-effects/
    │       ├── exists.js
    │       └── none.js
    ├── src/
    │   ├── handlers/
    │   │   ├── Base.js
    │   │   ├── Med.js
    │   │   ├── Verify.js
    │   │   └── _New.js
    │   ├── helpers/
    │   │   ├── Speech.js
    │   │   ├── messages.js
    │   │   ├── naming.js
    │   │   ├── refill.js
    │   │   ├── sideEffects.js
    │   │   └── verify.js
    │   ├── _dummyenv
    │   ├── _env (hidden)
    │   ├── analytics.js
    │   ├── api.js
    │   ├── config.js
    │   ├── consts.js
    │   ├── data.js
    │   ├── index.js
    │   ├── intercept.js
    │   └── server.js
    ├── test/
    │   ├── __README.md
    │   ├── _launch.js
    │   ├── _new_user.js
    │   ├── _unhandled.js
    │   ├── about_intent.js
    │   ├── describe_intent.js
    │   ├── getrx_color.js
    │   ├── getrx_condition.js
    │   ├── list_intent.js
    │   ├── medbox_eval.js
    │   ├── medbox_eval_directions.js
    │   ├── medbox_exec.js
    │   ├── medbox_exec_nomed.js
    │   ├── medbox_exec_pmed.js
    │   ├── next_^refill.js
    │   ├── next_refill.js
    │   ├── verify_start.js
    │   └── verify_step.js
    ├── utils/
    │   ├── data/
    │   │   ├── colors.js
    │   │   ├── conditions.js
    │   │   ├── medtypes.js
    │   │   ├── shapes.js
    │   │   └── timings.js
    │   ├── README.md
    │   └── builder.js
    ├── README.md
    ├── claudia.json
    ├── gulpfile.js
    ├── package.json
    ├── test_results.log (untracked) [$ npm test > test_results.log]
    └── tree.log (untracked) [$ tree -F -o tree.log -L 3  --filelimit 20  --dirsfirst]

### State Machine

#### MAIN STATE     (Default Entry Point for App)

    ENDS SESSION:
        DescribeIntent drug {DrugIndex}
        DescribeIntent tell me about drug {DrugIndex}
        DescribeIntent information on drug {DrugIndex}
        ==================================================
        ListIntent get meds
        ListIntent list meds
        ListIntent get my meds
        ListIntent list my meds
        ListIntent list my medications
        ==================================================
        AboutIntent about
        AboutIntent about author
        AboutIntent about developer
        ==================================================
        EvalIntent {Color | Condition | Timing} {Medtype}
        EvalIntent {Color} {Timing | Condition | Shape} {Medtype}
        EvalIntent {Shape} {Color | Condition} {Medtype}
        EvalIntent {Timing} { Condition} {Medtype}
        EvalIntent {Color} {Shape} {Timing} {Medtype}
        EvalIntent {Color} {Timing} {Condition} {Medtype}

    MAIN => MEDBOX:
        MedBoxIntent open med box
        MedBoxIntent open R X box
        MedBoxIntent open box
        ==================================================
        ExecIntent {DrugField}

    MAIN => DIRECTIONS:
        DirectionsIntent directions

    MAIN => REFILL:
        RefillIntent refill

    MAIN => VERIFY:
        VerifyStartIntent start verification
        VerifyStartIntent verify meds


#### MEDBOX STATE     (Dedicated Med Management State)

    ENDS SESSION:
        ListIntent ...
        ==================================================
        WITH medId:
            ExecIntent {...}
        ==================================================
        WITH medField:
            EvalIntent {...}

    MEDBOX => MEDBOX:
        WITHOUT medField:
            EvalIntent {...}
        ==================================================
        WITHOUT medId:
            ExecIntent {...}

    MEDBOX => DIRECTIONS:
        DirectionsIntent directions

    MEDBOX => REFILL:
        RefillIntent refill

    MEDBOX => VERIFY:
        VerifyStartIntent start verification
        VerifyStartIntent verify meds


#### DIRECTIONS STATE   (Directions Transitory State)

    ENDS SESSION:
        EvalIntent {...}


#### REFILL STATE   (Med Refill Management State)

    ENDS SESSION:
        NextRefillIntent next refill
        NextRefillIntent soonest refill
        NextRefillIntent next refill date
        NextRefillIntent soonest refill date
        ==================================================
        EvalIntent {...}


#### VERIFICATION STATE    (Med Verification State)

    IF COMPLETE:
        ENDS SESSION:
            VerifyStepIntent {Affirm | Reject | Maybe}
    ELSE:
        VERIFY => VERIFY:
            VerifyStepIntent {Affirm | Reject | Maybe}
