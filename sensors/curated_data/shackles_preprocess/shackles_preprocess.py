# Gathers data from files in ./shackles_preprocess/ and scales each column with given equations. Writes data to all_shackles_preprocessed.txt
# Must be run from curated_data folder
import pandas as pd
import datetime
import glob
import os

try:
    os.remove("./shackles_preprocess/all_shackles_preprocessed_not_csv.txt")
    os.remove("all_shackles_preprocessed.txt")
except OSError:
    pass

# get a list of all txt files.
txt_files = glob.glob('./shackles_preprocess/*.txt*')
df = pd.DataFrame()

for file in txt_files:
    # read text file into pandas DataFrame. analog channels 0, 6, and 7 weren't active when recording data and thus excluded
    df_i = pd.read_csv(file, sep="\t", skiprows=0, usecols=[0,2,3,4,5,6], header=1)
    df_i["Timestamp"] = pd.to_datetime(df_i["Timestamp"], format="%Y.%m.%d %H:%M:%S.%f")
    df_i.rename(columns={"Timestamp": "timestamp"}, inplace= True)

    # open corresponding text file and extract scaling equations
    with open(file) as f:
        firstline = f.readline().split("\t")
        equations = firstline[2:7] # equations like [ch1_eq, ch2_eq, ..., ch5_eq]
        multipliers = [float(s.split("*x")[0]) for s in equations]
        constants = [float(s.split("*x")[1]) for s in equations]

    # apply scaling equations to each analog channel and drop old values (only keep scaled values).
    for i in range(5):
        df_i[f"shackle-ch{i+1}"] = (df_i[f"Analog channel {i+1}"]*multipliers[i] + constants[i]).round(decimals=4)
        df_i.drop(columns=f"Analog channel {i+1}", inplace=True)

    # Make sure timestamps end in 0, 0.25, 0.5, or 0.75 instead of 0.095 and 0.161
    millisec_remainder = df_i["timestamp"][0].microsecond/1000 % 250
    df_i["timestamp"] -= datetime.timedelta(milliseconds = millisec_remainder)

    df = pd.concat([df, df_i], ignore_index=True)

df.sort_values(by="timestamp", inplace=True)
print(df)

with open("all_shackles_preprocessed.txt", 'w') as f:
    df_csv = df.to_csv(header=True, index=False, lineterminator="\n")
    f.write(df_csv)

with open("./shackles_preprocess/all_shackles_preprocessed_not_csv.txt", 'w') as f:
    df_string = df.to_string(header=True, index=False)
    f.write(df_string)
