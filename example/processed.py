import pandas as pd
#data1 = pd.read_csv("solar_data_202003_202007_processed.csv")
path = "D:/jerry/台科/綠能/AIoT_final/weather_data/"
data = pd.read_csv("processed.csv")
sun_list = []
for i in range (data.shape[0]):
    h = int(data.iloc[i]["HOUR"])
    #print(h)
    m = data.iloc[i]["MONTH"]
    d = data.iloc[i]["DAY"]
    if d < 10:
            d1 = "0" + str(int(d))
    else:
        d1 = str(int(d)) 
    if m < 10:
        m1 = "0" + str(int(m))
    else:
        m1 = str(int(m))
    date = str(int(data.iloc[i]["YEAR"]))+ "-" + m1 + "-" + d1
    s_data = pd.read_csv(path + date + "-1.csv")
    sun = s_data["全天空日射量(MJ/㎡)"][h]
    sun_list.append(sun)
print(sun_list)
data['SUN'] = sun_list
"""
sun = pd.DataFrame(columns = ["全天空日射量(MJ/㎡)"])
day = [31,29,31,30,31,30,31,31,30,31,30,31]
count = 0
for m in range(3,7):
    for d in range(1,day[m-1] + 1):
        count += 13
        if d < 10:
            d1 = "0" + str(d)
        else:
            d1 = str(d) 
        if m < 10:
            m1 = "0" + str(m)
        else:
            m1 = str(m)
        file = "2020-" + m1 + "-" + d1 
        data = pd.read_csv(path + file + "-1.csv")
        #tmp = pd.DataFrame([data["全天空日射量(MJ/㎡)"][6:19]] , columns = ["全天空日射量(MJ/㎡)"])
        #print(tmp)
        #print(type(data))
        tmp = list(data["全天空日射量(MJ/㎡)"][8:21])
        for i in tmp:
            sun = sun.append({"全天空日射量(MJ/㎡)" : i} , ignore_index = True)
        #sun = pd.Series(data = [sun,data["全天空日射量(MJ/㎡)"][6:19]] , index = ["全天空日射量(MJ/㎡)"])
"""
data.to_csv("final.csv" , index = False)