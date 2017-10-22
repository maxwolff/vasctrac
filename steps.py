import os
import numpy as np
import pandas as pd
from os.path import dirname, basename, abspath, join, exists
from scipy.signal import argrelextrema

# Internals
from utils import load_train, load_csv, ACTI_GRAPH

def get_steps(tr, idx):
    return tr.loc[tr['PID'] == idx, 'MANUAL_STEPS'].values[0]

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
