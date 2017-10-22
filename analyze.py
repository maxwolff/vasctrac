import os
from os.path import dirname, basename, abspath, join, exists
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

# Internals
from utils import load_train, OUT_DIR

def eval_preds(labeled_preds, truth_col, metric, method):
    tr = load_train()
    truth = tr[['PID', truth_col]]
    pred_col = 'PRED'
    # Only joins on rows where PID matches
    m = pd.merge(truth, labeled_preds, on=['PID'], how='inner')
    # Remove cases where truth is null
    m = m[pd.notnull(m[truth_col])]
    m['DIFF'] = m[truth_col].subtract(m[pred_col])
    m['PCT_DIFF'] = (100. * m['DIFF']) / m[truth_col]
    avg_dif = "%.2f " % np.abs(m['DIFF']).mean()
    std_dif = "%.2f " % m['DIFF'].std()
    avg_pct_dif = "%.2f " % np.abs(m['PCT_DIFF']).mean()
    mse = "%.2f " % mean_squared_error(m[truth_col], m[pred_col])
    print "Avg. Dif: {} | Std. Dif {} | Avg. Pct. Dif {} | MSE {}".format(
        avg_dif, std_dif, avg_pct_dif, mse)

    results_file = join(OUT_DIR, "{}_results_{}.csv".format(metric, method))
    m.to_csv(results_file)
