# Gathers data from all .txt files in ./depth_preprocess/ and writes them to all_depths.txt
# Must be run from curated_data folder
import pandas as pd
import datetime
import os

try:
    os.remove("./depth_preprocess/all_depths_not_csv.txt")
    os.remove("all_depths.txt")
except OSError:
    pass

# read text file into pandas DataFrame
df = pd.DataFrame(data={"timestamp": []})

for i in range(1, 17):
    if i == 15: # sensor nr 15 doesnt exist...
        continue
    else:
        df_i = pd.read_csv(f"./depth_preprocess/{i}.txt", sep="\t", names=["timestamp", f"depth{i}"], usecols=[1,3], decimal=',')
        df_i["timestamp"] = pd.to_datetime(df_i["timestamp"], format="%d.%m.%Y %H:%M:%S")

        if i == 5: # sensor nr 5 is ahead by 2 mintues
            df_i["timestamp"] -= datetime.timedelta(minutes=2)
        elif i == 12: # sensor nr 12 is ahead by 1 minute
            df_i["timestamp"] -= datetime.timedelta(minutes=1)

        df = pd.merge(df, df_i, on="timestamp", how="outer")

df.sort_values(by="timestamp", inplace=True)
print(df)

with open("all_depths.txt", 'w') as f:
    print("saving to csv")
    df_csv = df.to_csv(header=True, index=False, lineterminator="\n")
    f.write(df_csv)

with open("./depth_preprocess/all_depths_not_csv.txt", 'w') as f:
    print("saving to string")
    df_string = df.to_string(header=True, index=False)
    f.write(df_string)