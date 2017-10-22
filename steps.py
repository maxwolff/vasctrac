import argparse
import os
import numpy as np
import pandas as pd
from os.path import dirname, basename, abspath, join, exists
from scipy.signal import argrelextrema

# Internals
from utils import load_train, load_csv, ACTI_GRAPH
from analyze import eval_preds

def calc_magnitudes(df):
    """Should do some filtering here"""
    # See:
    # - https://github.com/danielmurray/adaptiv
    # - https://dsp.stackexchange.com/questions/40533/triaxial-accelerometer-to-single-signal
    # - http://scottlobdell.me/2014/08/kalman-filtering-python-reading-sensor-input/
    # Need the magnitude since we don't know the orientation
    ax, ay, az = df['X'].as_matrix(),  df['Y'].as_matrix(), df['Z'].as_matrix()
    return np.sqrt(np.power(ax,2) + np.power(ay,2) + np.power(az,2))

def calc_steps(name, bin_size=30):
    df = load_csv(name)
    A = calc_magnitudes(df)
    return len(argrelextrema(A, np.less, order=bin_size)[0])

def get_labeled_preds(limit=10):
    indices = []
    preds = []
    for name in os.listdir(ACTI_GRAPH)[:limit]:
        indices.append(int(basename(name).split(".csv")[0]))
        preds.append(calc_steps(name))
    data = np.array((indices, preds)).T
    return pd.DataFrame(data=data, columns=['PID', 'PRED'])

def eval_ours():
    labeled_preds = get_labeled_preds(121)
    eval_preds(labeled_preds, "MANUAL_STEPS", "steps", "OURS")

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
