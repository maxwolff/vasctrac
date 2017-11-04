import os
from os.path import dirname, basename, abspath, join, exists
import pandas as pd
import numpy as np

# Internals
from utils import load_train, OUT_DIR

def eval_preds(labeled_preds, truth_col, metric, method):
    tr = load_train()
    truth = tr[['PID', truth_col]]
    # Only joins on rows where PID matches
    m = pd.merge(truth, labeled_preds, on=['PID'], how='inner')
    m['DIFF'] = m[truth_col].subtract(m['PRED'])
    m['PCT_DIFF'] = (100. * m['DIFF']) / m[truth_col]
    avg_dif = np.abs(m['DIFF']).mean()
    std_dif = m['DIFF'].std()
    avg_pct_dif = np.abs(m['PCT_DIFF']).mean()
    print "Avg. Dif: {} | Std. Dif {} | Avg. Pct. Dif {}".format(
        avg_dif, std_dif, avg_pct_dif)

    results_file = join(OUT_DIR, "{}_results_{}.csv".format(metric, method))
    m.to_csv(results_file)
