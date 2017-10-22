import os
from os.path import dirname, basename, abspath, join, exists
import pandas as pd
import numpy as np
import argparse

# Internals
from utils import load_train, OUT_DIR
from steps import calc_steps, get_labeled_preds

def eval_preds(labeled_preds, method):
    TRUTH_COL = 'MANUAL_STEPS'
    tr = load_train()
    truth = tr[['PID', TRUTH_COL]]
    # Only joins on rows where PID matches
    m = pd.merge(truth, labeled_preds, on=['PID'], how='inner')
    m['DIFF'] = m[TRUTH_COL].subtract(m['PRED'])
    m['PCT_DIFF'] = (100. * m['DIFF']) / m[TRUTH_COL]
    avg_dif = m['DIFF'].mean()
    std_dif = m['DIFF'].std()
    avg_pct_dif = np.abs(m['PCT_DIFF']).mean()
    print "Avg. Dif: {} | Std. Dif {} | Avg. Pct. Dif {}".format(
        avg_dif, std_dif, avg_pct_dif)

    results_file = join(OUT_DIR, "results_{}.csv".format(method))
    m.to_csv(results_file)

def eval_ours():
    labeled_preds = get_labeled_preds(121)
    eval_preds(labeled_preds, "OURS")

def eval_actigraph():
    tr = load_train()
    labeled_preds = tr[['PID', 'ACTIGRAPH_STEPS']]
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "ACTIGRAPH")

def eval_vastrac():
    tr = load_train()
    labeled_preds = tr[['PID', 'VASCTRAC_STEPS']]
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "VASCTRAC")

def eval_naive():
    tr = load_train()
    labeled_preds = tr[['PID', 'VASCTRAC_STEPS']]
    labeled_preds['VASCTRAC_STEPS'] = 540 * np.ones(len(tr))
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "NAIVE")

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
