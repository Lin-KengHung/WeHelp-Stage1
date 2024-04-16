import urllib.request as request
import json


# 先讀資料
spot_src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
MRT_src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

with request.urlopen(MRT_src) as response:
    MRT_data = json.load(response)
with request.urlopen(spot_src) as response:
    spot_data = json.load(response)

# 做 serial_no to 景點/區 的字典
node2mrt = {}
node2dist = {}
for dic in MRT_data["data"]:
    node2mrt[dic["SERIAL_NO"]] = dic["MRT"]
    node2dist[dic["SERIAL_NO"]] = dic["address"][5:8]

# 寫spot.csv 
mrt2spot={}
with open("spot.csv", mode="w", encoding="utf-8") as file:
    for spot in spot_data["data"]["results"]:
        # 對照serail_no印出區
        dist = node2dist[spot["SERIAL_NO"]]
        # 切出第一張圖
        image_url = "https" + spot["filelist"].split('https')[1]
        # 輸出
        line = [spot["stitle"], dist, spot["longitude"], spot["latitude"], image_url]
        file.write(",".join(line) + "\n")

        # 處理景點附近的捷運站(mrt to spot)
        mrt = node2mrt[spot["SERIAL_NO"]]
        if (mrt not in mrt2spot.keys()):
            mrt2spot[mrt] = spot["stitle"]
        else:    
            mrt2spot[mrt] += "," + spot["stitle"]

# 寫mrt.csv
with open("mrt.csv", mode="w", encoding="utf-8") as file:
     for mrt in mrt2spot.keys():
         file.write(mrt + "," + mrt2spot[mrt] + "\n")
