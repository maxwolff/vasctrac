import argparse
import os
import numpy as np
import pandas as pd
from os.path import dirname, basename, abspath, join, exists
from scipy.signal import argrelextrema

# Internals
from utils import load_train, load_csv, ACTI_GRAPH
from analyze import eval_preds

"""
Build a model that uses raw sensor data + covariates to predict
PAD severity. This task can include feature engineering approaches
(PCA, DTW, signal entropy, etc.) and/or feature selection, such as
LASSO (L1 penalty) that will result in a compact model with the fewest
informative features. Cross-validation for parameter tuning is
strongly encouraged.
"""

def get_labeled_preds(limit=10):
    indices = []
    preds = []
    for name in os.listdir(ACTI_GRAPH)[:limit]:
        indices.append(int(basename(name).split(".csv")[0]))
        preds.append(calc_steps(name))
    data = np.array((indices, preds)).T
    return pd.DataFrame(data=data, columns=['PID', 'PRED'])

def eval_ours(col):
    labeled_preds = get_labeled_preds(121)
    eval_preds(labeled_preds, col, "abi_t4", "OURS")

def eval_naive(col):
    tr = load_train()
    valid_ids = tr['PID'].values
    if col == "MIN_ABI":
        preds = 1.0 * np.ones(len(valid_ids))
    else:
         preds = 0.92 * np.ones(len(valid_ids))
    data = np.array((valid_ids, preds)).T
    labeled_preds =  pd.DataFrame(data=data, columns=['PID', 'PRED'])
    eval_preds(labeled_preds, col, "abi_t4", "NAIVE")

def main():
    parser = argparse.ArgumentParser(description="Main")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--naive', action='store_true')
    group.add_argument('-o', '--ours', action='store_true')
    colgroup = parser.add_mutually_exclusive_group()
    colgroup.add_argument('-m', '--min', action='store_true')
    colgroup.add_argument('-a', '--avg', action='store_true')
    args = parser.parse_args()
    col = "MIN_ABI" if args.min else "AVG_ABI" if args.avg else "MIN_ABI"
    if args.naive:
        eval_naive(col)
    else:
        eval_ours(col)

if __name__ == '__main__':
    main()
