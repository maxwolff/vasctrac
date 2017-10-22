import os
from os.path import dirname, basename, abspath, join
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

VASTRAC = "VascTrac_Hackathon"
ACTI_GRAPH = join(VASTRAC, "ActiGraph")

def setup():
    os.chdir(dirname(__file__))

def load_train():
    name="train.csv"
    columns = ["Timestamp", "X", "Y", "Z" ]
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
    return np.array((indices, preds)).T

labeled_preds = get_labeled_preds(100)
tr = load_train()

steps = tr['MANUAL_STEPS'].as_matrix()

m2()
