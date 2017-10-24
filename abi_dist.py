"""
Given left and right ABIs, come up with a better model to predict step/distance walked during 6MWT (ground truth distance).
"""
import argparse
import os
import numpy as np
import pandas as pd
from os.path import dirname, basename, abspath, join, exists
from scipy.signal import argrelextrema

# Internals
from utils import load_train
from analyze import eval_preds

def get_labeled_preds():
    tr = load_train()
    m = tr[['PID', 'RIGHT_ABI', 'LEFT_ABI']]
    m[np.logical_not(np.logical_and(pd.notnull(m["RIGHT_ABI"]),
    pd.notnull(m["LEFT_ABI"])))] = 0
    valid_ids = m['PID'].values
    x = np.minimum(m["RIGHT_ABI"].values, m["LEFT_ABI"].values)
    high = 1.5
    x[ x > high] = np.power(x[x > high ], -x[ x > high])
    x [ x > 1 ] = 1
    '''
    assume 1000 ft traveled if min_abi (m) is 1
    should cap factor at 1 or perhaps penalize for m > 1.02
    simple linear model:
      f(m) = 1000 * x
    '''
    preds = 1000 * x
    data = np.array((valid_ids, preds)).T
    return pd.DataFrame(data=data, columns=['PID', 'PRED'])

def eval_ours():
    labeled_preds = get_labeled_preds()
    eval_preds(labeled_preds, "TRACK_DISTANCE", "abi_dist", "OURS")

def eval_vastrac():
    tr = load_train()
    m = tr[['PID', 'RIGHT_ABI', 'LEFT_ABI', 'VASCTRAC_DISTANCE']]
    m = m[np.logical_and(pd.notnull(m["RIGHT_ABI"]),
                        pd.notnull(m["LEFT_ABI"]))]
    valid_ids = m['PID'].values
    preds = m['VASCTRAC_DISTANCE'].values
    data = np.array((valid_ids, preds)).T
    labeled_preds = pd.DataFrame(data=data, columns=['PID', 'PRED'])
    eval_preds(labeled_preds, "TRACK_DISTANCE", "abi_dist", "VASCTRAC")

def eval_naive():
    tr = load_train()
    labeled_preds = tr[['PID', 'VASCTRAC_STEPS']]
    labeled_preds['VASCTRAC_STEPS'] = 1000 * np.ones(len(tr))
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "TRACK_DISTANCE", "abi_dist", "NAIVE")

def main():
    parser = argparse.ArgumentParser(description="Main")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--vastrac', action='store_true')
    group.add_argument('-n', '--naive', action='store_true')
    group.add_argument('-o', '--ours', action='store_true')
    args = parser.parse_args()
    if args.vastrac:
        eval_vastrac()
    elif args.naive:
        eval_naive()
    else:
        eval_ours()

if __name__ == '__main__':
    main()
