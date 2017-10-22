import os
from os.path import dirname, basename, abspath, join, exists
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, butter, lfilter, freqz
import matplotlib.pyplot as plt

VASTRAC = "VascTrac_Hackathon"
ACTI_GRAPH = join(VASTRAC, "ActiGraph")
OUT_DIR = "build"

def setup():
    os.chdir(dirname(abspath(__file__)))
    if not exists(OUT_DIR):
        os.mkdir(OUT_DIR)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def load_train():
    name="train.csv"
    with open(join(VASTRAC, name)) as infile:
        df = pd.read_csv(infile, sep=',')
        df.drop([col for col in df.columns if "Unnamed" in col], axis=1, inplace=True)
    return df

def get_steps(tr, idx):
    return tr.loc[tr['PID'] == idx, 'MANUAL_STEPS'].values[0]


def load_csv(name):
    name = name if name.endswith(".csv") else "{}.csv".format(name)
    columns = ["Timestamp", "X", "Y", "Z" ]
    with open(join(ACTI_GRAPH, name)) as infile:
        df = pd.read_csv(infile, sep=',', skiprows=11, names=columns)
        # df = df[df.columns[~df.columns.str.contains('Unnamed:')]
        # df.drop([col for col in df.columns if "Unnamed" in col], axis=1, inplace=True)
    return df

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

def m1():
    limit = 10
    tr = load_train()
    for name in os.listdir(ACTI_GRAPH)[:limit]:
        idx = int(basename(name).split(".csv")[0])
        pred = calc_steps(name)
        try:
            truth = get_steps(tr, idx)
            pct_diff = "%.f" % (100 * float(truth - pred) / truth)
            print "File: {} | Pred: {} | Truth: {} | {}%".format(name, pred, truth, pct_diff)
        except Exception as e:
            print "File: {} -- {}".format(name, e)

def get_labeled_preds(limit=10):
    indices = []
    preds = []
    for name in os.listdir(ACTI_GRAPH)[:limit]:
        indices.append(int(basename(name).split(".csv")[0]))
        preds.append(calc_steps(name))
    data = np.array((indices, preds)).T
    return pd.DataFrame(data=data, columns=['PID', 'PRED'])

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

if __name__ == '__main__':
    # Setup
    setup()
    eval_ours()
    eval_actigraph()
    eval_vastrac()
    eval_naive()
