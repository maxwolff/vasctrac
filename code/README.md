## Inspiration

The field of healthcare is broadly focused on providing late stage disease treatments instead of prevention, leading to poor health outcomes and high costs. PAD (peripheral arterial disease) is low-hanging fruit to start this shift in our mindset. It's an easily diagnosed disease with known covariates and a clear a treatment plan. Working on diagnostic tools and treatment adherence could have a huge impact!

## What it does

We took on the Vastrac Data challenge, building ABI (a predictor of PAD) prediction algorithms using raw sensor data from a handheld accelerometer during a 6-minute walking test. 

We wanted to take this even further, recognizing the power in building good human-computer interfaces could have in aiding early diagnosis and treatment adherence. 

PAD-Piper is an Alexa skill for PAD patients, built to amplify the impact of our algorithms. Voice is a great interface PAD patients, who skew to be older and often have difficulty using mobile phones. PAD-Piper integrates with your phone pedometer, tracking your steps per day, and predicting the change in the severity of your PAD week over week. You can also ask where the closest family practice doctors are. 

eg: 
Q: How’s my pad?
A: “Your ABI improved 10% this week based on your stride. You walked 5000 steps this week, which is 20% above your goal. Keep up the good work! “

## How I built it

To build the prediction algorithms, we first normalized the x,y,z acceleration data into magnitude. Then we applied some DSP techniques to find steps and distance walked, which we then used to predict ABI. 

We used a Node.js backend to work with the Alexa SDK. We also integrated the BetterHealth API to find doctor information. 

## Challenges I ran into

Working with noisy sensor data was the biggest challenge.

## Accomplishments that I'm proud of

We're proud of conceptualizing an application for the algorithm we built. 

## What I learned

We got a great appreciation for the whole "stack" of disease prevention and diagnosis: from clinical insight to raw sensor data to prediction and human-computer interface. 

## What's next for P.A.D. Piper? 

We'd love to see this skill implemented as part of Vastrac! 