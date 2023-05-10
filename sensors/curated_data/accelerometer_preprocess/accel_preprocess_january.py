# Gathers data from files in ./accelerometer_preprocess/ and writes to all_accel_preprocessed.txt
# Must be run from curated_data folder
import pandas as pd

df = pd.read_csv("./accelerometer_preprocess/january.csv", sep=",", header=0)

# round decimals and convert Time from string to datetimes
df.iloc[:,1:] = df.iloc[:,1:].round(decimals=4)
df["Time"] = pd.to_datetime(df["Time"], format="%m/%d/%y %H:%M:%S.%f")

# drop sensor 14749:ch2 (sensor number 4) as it was down all of january (8 of 10 time periods for analysis)
df.drop(columns='14749:ch2', errors="ignore", inplace=True)

# drop rows that contain NAN values (missing values)
df.dropna(inplace=True, ignore_index=True)

# rename columns
df.rename(columns={'Time': 'timestamp', '14746:ch2': 'accel1-14746','14747:ch2': 'accel2-14747', '14748:ch2': 'accel3-14748',
                            '14752:ch2': 'accel5-14752', '14753:ch2': 'accel6-14753', '14754:ch2': 'accel7-14754', '14755:ch2': 'accel8-14755'}, inplace= True)

# sort by date
df.sort_values(by="timestamp", inplace=True)
print(df.tail())

with open("all_accel_january.txt", 'w') as f:
    print("saving to csv")
    df_csv = df.to_csv(header=True, index=False, lineterminator="\n")
    f.write(df_csv)

print("done.")