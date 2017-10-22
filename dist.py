import numpy as np
import argparse

# Internals
from utils import load_train
from steps import get_labeled_preds
from analyze import eval_preds

def predict_dist(limit):
    labeled_preds = get_labeled_preds(limit)
    avg_step_length = 1.7
    labeled_preds['PRED'] *= avg_step_length
    return labeled_preds

def eval_ours():
    labeled_preds = predict_dist(121)
    eval_preds(labeled_preds, "TRACK_DISTANCE", "dist", "OURS")

def eval_vastrac():
    tr = load_train()
    labeled_preds = tr[['PID', 'VASCTRAC_DISTANCE']]
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "TRACK_DISTANCE", "dist", "VASCTRAC")

def eval_naive():
    tr = load_train()
    labeled_preds = tr[['PID', 'VASCTRAC_DISTANCE']]
    labeled_preds['VASCTRAC_DISTANCE'] = 1000 * np.ones(len(tr))
    labeled_preds.columns = ['PID', 'PRED']
    eval_preds(labeled_preds, "TRACK_DISTANCE", "dist", "NAIVE")

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
