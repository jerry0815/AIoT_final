from flask import Flask, request, jsonify
from keras.models import load_model
import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

app = Flask(__name__)
model = load_model('aiot.h5')

df = pd.read_csv('final.csv')
df = df[df['kwh']<30]

X = df[['HOUR','OPTPWR','IIT','IHT','SUN']]
Y = df[['kwh']]
min_max_scaler_X = MinMaxScaler()
min_max_scaler_Y = MinMaxScaler()
X_scale = min_max_scaler_X.fit_transform(X)
Y_scale = min_max_scaler_Y.fit_transform(Y)
path = "D:/jerry/台科/綠能/AIoT_final/weather_data/"
def process(y,m,d):
    if int(m) < 10:
        m = "0" + str(int(m))
    else :
        m = str(int(m))
    if int(d) < 10:
        d = "0" + str(int(d))
    else :
        d = str(int(d))
    return str(int(y)) + "-" + m + "-" + d

@app.route('/predict', methods=['POST'])
def predict():
    body = request.data.decode('utf-8')
    dataset = json.loads(body)
    new_data = []
    for d in dataset['questions']:
        date = process(d[0],d[1],d[2])
        h = int(d[3])
        s_data = pd.read_csv(path + date + "-1.csv")
        sun = s_data["全天空日射量(MJ/㎡)"][h]
        new_data.append([d[3], d[4], d[10], d[11],sun])
    t_test = min_max_scaler_X.transform(np.array(new_data))
    pre = model.predict(t_test)
    resp = {'predictions': min_max_scaler_Y.inverse_transform(pre).tolist() }
    return jsonify(resp)

if __name__ == "__main__":
    app.debug = True
    app.run()