# Gathers data from files in ./accelerometer_preprocess/ and writes to all_accel_preprocessed.txt
# Must be run from curated_data folder
import pandas as pd
import glob
import os

try:
    os.remove("./accelerometer_preprocess/all_accel_preprocessed_not_csv.txt")
    os.remove("all_accel_preprocessed.txt")
except OSError:
    pass

# get list of all csv files
csv_files = glob.glob('./accelerometer_preprocess/*.csv*')
df = pd.DataFrame()

for file in csv_files:
        df_i = pd.read_csv(file, sep=",", header=0)
        
        # round decimals and convert Time from string to datetimes
        df_i.iloc[:,1:] = df_i.iloc[:,1:].round(decimals=4)
        df_i["Time"] = pd.to_datetime(df_i["Time"], format="%m/%d/%y %H:%M:%S.%f")

        # drop sensor 14749:ch2 (sensor number 4) as it was down all of january (8 of 10 time periods for analysis)
        df_i.drop(columns='14749:ch2', errors="ignore", inplace=True)
        
        # drop rows that contain NAN values (missing values)
        df_i.dropna(inplace=True, ignore_index=True)

        # rename columns
        df_i.rename(columns={'Time': 'timestamp', '14746:ch2': 'accel1-14746','14747:ch2': 'accel2-14747', '14748:ch2': 'accel3-14748',
                            '14752:ch2': 'accel5-14752', '14753:ch2': 'accel6-14753', '14754:ch2': 'accel7-14754', '14755:ch2': 'accel8-14755'}, inplace= True)
        
        df = pd.concat([df, df_i], ignore_index=True)

# sort by date
df.sort_values(by="timestamp", inplace=True)
print(df)

with open("all_accel_preprocessed.txt", 'w') as f:
    df_csv = df.to_csv(header=True, index=False, lineterminator="\n")
    f.write(df_csv)

with open("./accelerometer_preprocess/all_accel_preprocessed_not_csv.txt", 'w') as f:
    df_string = df.to_string(header=True, index=False)
    f.write(df_string)