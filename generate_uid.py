import pandas as pd
import datetime


def generate_new_id():
    # new ID generation
    df = pd.read_csv("uid.csv", header=0)
    if df.empty:
        print("Dataframe is empty")
        new_ID = "UID0001"
    else:
        last_ID = df["UID"].iloc[-1]
        digit = int(last_ID[-4:])
        # print(digit)
        digit += 1
        new_ID = "UID" + str(digit).zfill(4)
    # df = df.append({
    #     "UID": new_ID,
    #     "TimeStamp": datetime.datetime.now()
    # }, ignore_index=True)
    #
    # df.to_csv('uid.csv', index=False, header=True)
    return new_ID