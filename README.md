# Summary 
We worked with the [Vasctrac](http://vasctrac.stanford.edu/) team to build predictors for peripheral arterial disease (PAD) biomarkers. The input was raw sensor data (iphone accelerometer, sans gyro) from 113 patients taking a diagnostic known as the 6 minute walking test. 

- Scales and filters sensor data predict Ankle Brachial Index (ABI) a biomarker for PAD, steps walked, and distance walked
- Step counter is 92% accurate (iPhone is 94%)
- fatigue measure had .25 correlation coefficient with AVG_ABI

Winner of the Vasctrac Data Challenge at the Stanford Health ++ Hackathon, Oct. 2017 (along with @zzeleznick). Written that weekend and extended in the following weeks. 

# Methods

First, we took the magnitude of the (x,y,z) sensor readings (steps.py). Next, we used a low-pass butterworth filter to smooth noise in the data (steps.py).  We found steps by looking for relative extrema in the magnitude (steps.py). We found a window of .6 seconds worked best, roughly our average stride duration (30 data points on each side * .01 seconds * both sides = .6 second window on each side). 

To predict distance, we calculated expected steps and multiplied by a constant representing average step length. We found this to be 1.7 feet (dist.py). 

One hurdle in our analysis was that the elderly population at highest risk for PAD is also at high risk for several other gait-effecting conditions (arthritis, bad hip, etc). Vasctrac hypothesized that the charactaristic swelling pain from PAD could differentiate PAD-induced walking difficulty from the more consistent pain from other conditions. To test this, we created found the ratio of # steps taken during seconds 0 - 100 to steps taken in seconds and 100 - 400 (abi_t4.py). We found this measure had a .25 correlation with ABI, not huge, but enough to be interesting. 


# Usage 

add [data](https://stanfordmedicine.app.box.com/s/nxfozpy2n68aldqmmkkjmkc96hg8juqj) in a folder called VascTrac_Hackathon. Get permissions from the Vasctrac team.

Continued development on 
- steps.py much of the logic
- abi_t4.py evaluates accuracy

Hackathon challenge files: 
- dist.py given steps, find distance walked
- abi_dist.py: given ABIs, find distance walked

utils: 
- analyze.py - evaluate predictions for the challenges. used across data sources (abi & steps via flags)
- utils.py - read csv and other util functions 

usage: python abi_t4.py etc. our hackathon submission is in 'submission'

other files: [Adaptiv](https://github.com/danielmurray/adaptiv) is a project with great algorithms for this type of work. Unfortunately, have not finished integrating these.

# Guiding Research
 
- [6 min walking test](https://www.ncbi.nlm.nih.gov/pubmed/24982117)
- [ABI validity](https://www.ncbi.nlm.nih.gov/pubmed/15280343)
- [Accelerometer gait analysis ](http://www.tandfonline.com/doi/abs/10.1080/17445760.2015.1044007)
 
# Todo

- get rid of noisy patients
- use iphone pedometer to predict ABI
- integrate adaptiv algorithms. missing piece is tuning params. working in adaptiveStepJerkThreshold.py
- master regression for ABI with 'fatigue' measure, step count, demographics (diabetes y/n, age, smoking) etc. 
