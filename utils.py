import os
import pandas as pd
from os.path import dirname, basename, abspath, join, exists
from scipy.signal import butter, lfilter, freqz

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
    # with open(join(VASTRAC, name)) as infile:
    with open(name) as infile:
        df = pd.read_csv(infile, sep=',')
    df.drop([col for col in df.columns if "Unnamed" in col], axis=1, inplace=True)
    df = df.replace( {"WALKER_AID_6MWT": {"NONE": 0, "WALKER": -1, "CANE": 1 }} )
    return df

def load_csv(name):
    name = name if name.endswith(".csv") else "{}.csv".format(name)
    columns = ["Timestamp", "X", "Y", "Z" ]
    with open(join(ACTI_GRAPH, name)) as infile:
        df = pd.read_csv(infile, sep=',', skiprows=11, names=columns)
    return df

def show():
    df = load_train()
    print df[["PID", "WALKER_AID_6MWT"]][:10]

setup()

if __name__ == '__main__':
    show()