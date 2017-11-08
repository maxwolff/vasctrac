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

const HELP_MESSAGES = {
    BASE: {
        speech: base_help_speech,
        card: base_help_card
    }
}

const base_launch_speech = `
<p>Welcome to Pad Piper</p>
<s>You can say a command like, what is PAD</s>
<s>Or how can I improve?</s>`.replace(/\n/g, '')

const base_launch_card = `
<p>Welcome to Pad Piper </p>
You can say a command like, <i>what is PADs</i>.
Or <i>how can I improve</i> for personalized recommendations.
<p>For more on what you can say, please say <i>help me.</i></p>`.trim().replace(/<\/?[a-z]+>/g, "")

const LAUNCH_MESSAGES = {
    BASE: {
        speech: base_launch_speech,
        card: base_launch_card
    }
}

module.exports = {
    HELP_MESSAGES: HELP_MESSAGES,
    LAUNCH_MESSAGES: LAUNCH_MESSAGES
}