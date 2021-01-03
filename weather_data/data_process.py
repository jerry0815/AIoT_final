import pandas as pd
"""
data = pd.read_csv("2020-06-29.csv")
print(data["全天空日射量(MJ/㎡)"][1:])
"""

day = [31,29,31,30,31,30,31,31,30,31,30,31]
for m in range(1,13):
    for d in range(1,day[m-1] + 1):
        if d < 10:
            d1 = "0" + str(d)
        else:
            d1 = str(d) 
        if m < 10:
            m1 = "0" + str(m)
        else:
            m1 = str(m)
        file = "2020-" + m1 + "-" + d1 
        print(file)
        data = pd.read_csv(file + ".csv")
        data = data["全天空日射量(MJ/㎡)"][1:]
        data.to_csv(file + "-1.csv" , index = False , encoding='utf_8_sig')