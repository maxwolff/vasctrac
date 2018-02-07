import argparse
import os
import numpy as np
import pandas as pd
from os.path import dirname, basename, abspath, join, exists
from scipy.signal import argrelextrema

# Internals
from utils import load_train, load_csv, ACTI_GRAPH, IPHONE
from analyze import eval_preds
from scipy.signal import butter, lfilter, freqz
from adaptive_jerk_pace_buffer import adaptive_jerk_pace_buffer
from adaptiveStepJerkThreshold import adaptive_step_jerk_threshold
import pdb
from datetime import datetime, date, time



def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def calc_magnitudes(df):
    # See:
    # - https://github.com/danielmurray/adaptiv
    # - https://dsp.stackexchange.com/questions/40533/triaxial-accelerometer-to-single-signal to get magnitude
    # - http://scottlobdell.me/2014/08/kalman-filtering-python-reading-sensor-input/
    # Need the magnitude since we don't know the orientation
    ax, ay, az = df['X'].as_matrix(),  df['Y'].as_matrix(), df['Z'].as_matrix()
    r_data = np.sqrt(np.power(ax,2) + np.power(ay,2) + np.power(az,2))
    order = 3
    fs = 50.0  # sample rate, Hz
    cutoff = 3.667  # desired cutoff frequency of the filter, Hz
    r_data = butter_lowpass_filter(r_data, cutoff, fs, order) 
    return r_data, df["Timestamp"]

def toSecs(dt):
    dt = datetime.strptime(dt, "%m/%d/%Y %H:%M:%S.%f")
    return (dt - datetime(1970,1,1)).total_seconds()

def calc_step_indices(magnitudes,order):
    return argrelextrema(magnitudes, np.less, order=order)[0]

def calc_steps(name, device, bin_size=30):
    df = load_csv(name,device)
    B = calc_magnitudes(df)

    timestamps = np.array(B[1].apply(toSecs))
    magnitudes = calc_magnitudes(df)[0]
    return len(argrelextrema(magnitudes, np.less, order=bin_size)[0])
'''
    r = B[0] # magnitudes
    pdb.set_trace()
    #peaks, troughs, avgs = adaptive_jerk_pace_buffer(r,timestamps)
    jumps, avgs = adaptive_step_jerk_threshold(r,timestamps)
    peak_ts = [peak['ts'] for peak in peaks]
    peak_val = [peak['val'] for peak in peaks]
    trough_ts = [trough['ts'] for trough in troughs]
    trough_val = [trough['val'] for trough in troughs]
    print("Adaptive Jerk Pace Buffer Steps:", len(troughs))

    magnitudes = calc_magnitudes(df)[0]
    return len(argrelextrema(magnitudes, np.less, order=bin_size)[0])'''
def get_steps_preds(device, limit=10):
    indices = []
    preds = []
    for name in os.listdir(device)[:limit]:
        stripped = basename(name).split(".csv")[0]
        if device == IPHONE and 'ACCEL' in stripped:
            indices.append(int(stripped.replace("_ACCEL", "")))
            preds.append(calc_steps(name,'iphone'))
        elif device == ACTI_GRAPH: 
            indices.append(int(stripped))
            preds.append(calc_steps(name,'actigraph'))
    data = np.array((indices, preds)).T
    return pd.DataFrame(data=data, columns=['PID', 'PRED'])

def eval_ours():
    labeled_preds = get_steps_preds(ACTI_GRAPH,121)
    tr = load_train()


    eval_preds(labeled_preds, "MANUAL_STEPS", "steps", "OURS","MANUAL_STEPS")


def eval_actigraph():
    tr = load_train()
    labeled_preds = tr[['PID', 'ACTIGRAPH_STEPS']]
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "MANUAL_STEPS", "steps", "ACTIGRAPH")

def eval_vastrac():
    tr = load_train()
    labeled_preds = tr[['PID', 'VASCTRAC_STEPS']]
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "MANUAL_STEPS", "steps", "VASCTRAC")

def eval_naive():
    tr = load_train()
    labeled_preds = tr[['PID', 'VASCTRAC_STEPS']]
    labeled_preds['VASCTRAC_STEPS'] = 540 * np.ones(len(tr))
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "MANUAL_STEPS", "steps", "NAIVE")

def main():
    parser = argparse.ArgumentParser(description="Main")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--actigraph', action='store_true')
    group.add_argument('-v', '--vastrac', action='store_true')
    group.add_argument('-n', '--naive', action='store_true')
    group.add_argument('-o', '--ours', action='store_true')
    args = parser.parse_args()
    if args.vastrac:
        eval_vastrac()
    elif args.actigraph:
        eval_actigraph()
    elif args.naive:
        eval_naive()
    else:
        eval_ours()

if __name__ == '__main__':
    main()
