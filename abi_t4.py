import numpy as np
import argparse
import os
from os.path import dirname, basename, abspath, join, exists
import pandas as pd
from scipy.signal import argrelextrema
from datetime import datetime, date, time
import matplotlib.pyplot as plt
import pdb

# Internals
from utils import load_train,load_csv, ACTI_GRAPH,IPHONE
from steps import get_steps_preds
from analyze import eval_preds, select_min_abi, select_avg_abi
from steps import calc_magnitudes,calc_steps

def predict_dist(limit): # dont use in this file
    labeled_preds = get_steps_preds(limit)
    avg_step_length = 1.7
    labeled_preds['PRED'] *= avg_step_length
    return labeled_preds

def makeDateTimeObj(timeString): # used for reading actigraph timestamps
    obj = datetime.strptime(timeString, "%m/%d/%Y %H:%M:%S.%f")
    return obj

def get_steptimes(device,limit=200): # gets step times for 
    indices = []
    steps = []
    for name in os.listdir(device)[:limit]:
        stripped = basename(name).split(".csv")[0]
        if device == IPHONE and 'ACCEL' in stripped:
            indices.append(int(stripped.replace("_ACCEL", "")))
            steps.append(calc_step_times(name,'iphone'))
        elif device == ACTI_GRAPH: 
            indices.append(int(stripped))
            steps.append(calc_step_times(name,'actigraph'))
   # print 'all', steps
    df = pd.DataFrame(index = indices, data= steps)
    df.index.name = "PID"
    return df

def calc_step_times(name, device,bin_size=30):
    df = load_csv(name,device)
#   all_timestamps = df['Timestamp']
    A = calc_magnitudes(df)[0]
    indices = argrelextrema(A, np.less, order=bin_size)[0]
    timestamps = []
    if device == 'actigraph': 
        #return get_actigraph_timestamps(df,indices)
        print 'implement'
    if device == 'iphone': 
        for index in indices: 
            timestamps.append(df['Timestamp'].loc[index])
        return timestamps
        #return get_iphone_timestamp_delta(df,indices)

def get_actigraph_timestamp_delta(df,indices): # time between steps. dont use yet
    #loads deltas, not just timestamps
    timestamps = []
    last = makeDateTimeObj(df['Timestamp'][0])
    for i in indices[1:]:
        nextTimestamp = makeDateTimeObj(df['Timestamp'][i])
        timestamps.append((nextTimestamp - last).total_seconds())
        last = nextTimestamp 
    return timestamps

def get_iphone_timestamp_delta(df,indices): # time between steps. dont use yet. 
    #broken
    timestamps = []
    last = df['Timestamp'][0]
    for i in indices:
        nextTimestamp = df['Timestamp'].loc[i]
        timestamps.append(nextTimestamp - last)
        last = nextTimestamp 
    return timestamps

def eval_ours(): # wrong function. predicts steps, not abi
    labeled_preds = predict_dist(121)
    eval_preds(labeled_preds, "TRACK_DISTANCE", "dist", "OURS")

def eval_naive(col): # establish baseline for ABI preds. do not use.
    tr = load_train() #grab all PIDs from train set, make predictions
    valid_ids = tr['PID'].values
    if col == "MIN_ABI":
        preds = 1.0 * np.ones(len(valid_ids))
    else:
         preds = 0.92 * np.ones(len(valid_ids))
    data = np.array((valid_ids, preds)).T
    labeled_preds =  pd.DataFrame(data=data, columns=['PID', 'PRED'])
    eval_preds(labeled_preds, col, "abi_t4", "NAIVE",'PRED')


def get_fatigue_ratio(data): 
    arr = []
    for patientNum in data.index:
        count1 = 0
        count2 = 0
        for step in data.loc[patientNum]:
            if step < 100: 
                count1 += 1
            if 100 < step < 400: #  MODIFY ME!
                count2 += 1
        if count1 != 0 and count2 != 0: # remove 0s 
            arr.append([patientNum,count1,count2, (1.0*count1/count2)])
    f = np.array(arr).T
    return f


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
    data = get_steptimes(IPHONE)
    fatigue = get_fatigue_ratio(data)
    f = pd.DataFrame(data = fatigue.T,index = fatigue[0], columns = ["PID", "first", "second","ratio"])
    f = f[(f.T != 0).any()] # remove zeros
    tr = select_avg_abi(load_train())
    truth = tr[['PID', 'AVG_ABI']]
    m = f.merge(truth, on = 'PID')
    pdb.set_trace()
    print m.head()
    print "Fatigue Ratio Correlation", m['ratio'].corr(m['AVG_ABI'])

'''
# plots steps over time. biased bc not everyone reaches 500 steps etc. 
    plt.plot(get_steptimes(IPHONE))
    plt.ylabel('secs between steps')
    plt.xlabel('step #')
    plt.show() 
#    print get_steptimes()
'''


