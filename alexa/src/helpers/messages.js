const base_help_speech = `
<p>Here are some things you can say:</p>
<s>List my meds</s>
<s>Next refill</s>
<s>Directions</s>`.replace(/\n/g, '')

const base_help_card = `
<p>Here are some things you can say:</p>
<i>List my meds</i>
<i>Next refill</i>
<i>Directions</i>
<p>For more on what you can say, please say <i>help me.</i></p>`.trim().replace(/<\/?[a-z]+>/g, "")

const med_help_speech = `
<p>Here are some things you can say:</p>
<s>directions</s>
<s>refill</s>
<s>supply</s>
<s>last filled</s>
<s>dose</s>
<s>side effects</s>`.replace(/\n/g, '')

const med_help_card = `
<p>Here are some things you can say:</p>
<ul>
<li>directions</li>
<li>refill</li>
<li>supply</li>
<li>last filled</li>
<li>dose</li>
<li>side effects</li>
</ul>
<p>For more on what you can say, please say <i>help me.</i></p>`.trim().replace(/<\/?[a-z]+>/g, "")

const refill_help_speech = `
<p>If you'd like to find out the refill date for a specific medication say its name now</p>
<s>Or, you can say 'soonest refill' for your soonest refill date</s>`.replace(/\n/g, '')


const verify_help_speech = `
<p>It's always important to keep your medications up to date</p>
<s>We need your help to confirm our records</s>
<s>Please say 'start' when you are ready to begin</s>`.replace(/\n/g, '')


const verify_help_card = `
<p>It's always important to keep your medications up to date</p>
We need your help to confirm our records.
Please say 'start' when you are ready to begin.`.trim().replace(/<\/?[a-z]+>/g, "")


const HELP_MESSAGES = {
    BASE: {
        speech: base_help_speech,
        card: base_help_card
    },
    MED: {
        speech: med_help_speech,
        card: med_help_card
    },
    REFILL: {
        speech: refill_help_speech
    },
    VERIFY: {
        speech: verify_help_speech,
        card: verify_help_card
    }
}

const base_launch_speech = `
<p>Welcome to Humana</p>
<s>You can say a command like, list my medications</s>
<s>Or directions for drug information</s>`.replace(/\n/g, '')

const base_launch_card = `
<p>Welcome to Humana</p>
You can say a command like, <i>list my medications</i>.
Or <i>directions</i> for drug information.
<p>For more on what you can say, please say <i>help me.</i></p>`.trim().replace(/<\/?[a-z]+>/g, "")

const med_launch_speech = `
<p>Welcome to Humana MedBox</p>
<s>You can say a command like, list my meds</s>
<break time='200ms'/>
<s>Refill for personalized refill information</s>
<break time='200ms'/>
<s>Or directions for drug information</s>`.replace(/\n/g, '')

const med_launch_card = `
<p>Welcome to Humana MedBox</p>
You can say a command like, <i>list my meds</i>.
Say refill for personalized refill information.
Or <i>directions</i> for drug information.
<p>For more on what you can say, please say <i>help me.</i></p>`.trim().replace(/<\/?[a-z]+>/g, "")

const verify_launch_speech = `
<p>It's time to verify your medication</p>
<s>Please say 'start' to begin the verification</s>
<s>Or say 'snooze' to return to the main activity</s>`.replace(/\n/g, '')

const verify_launch_card = `
<p>It's time to verify your medication</p>
Please say <i>start</i> to begin the verification.
Or say <i>snooze</i> to return to the main activity.
<p>For more on what you can say, please say <i>help me.</i></p>`.trim().replace(/<\/?[a-z]+>/g, "")

const LAUNCH_MESSAGES = {
    BASE: {
        speech: base_launch_speech,
        card: base_launch_card
    },
    MED: {
        speech: med_launch_speech,
        card: med_launch_card
    },
    VERIFY: {
        speech: verify_launch_speech,
        card: verify_launch_card
    }
}

module.exports = {
    HELP_MESSAGES: HELP_MESSAGES,
    LAUNCH_MESSAGES: LAUNCH_MESSAGES
}