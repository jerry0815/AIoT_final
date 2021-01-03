from flask import Flask, request, jsonify
from keras.models import load_model
import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

app = Flask(__name__)
model = load_model('aiot.h5')

df = pd.read_csv('./solar_data_202003_202007_processed.csv')
df = df[df['kwh']<30]

X = df[['HOUR','OPTPWR','IIT','IHT']]
Y = df[['kwh']]
min_max_scaler_X = MinMaxScaler()
min_max_scaler_Y = MinMaxScaler()
X_scale = min_max_scaler_X.fit_transform(X)
Y_scale = min_max_scaler_Y.fit_transform(Y)

@app.route('/predict', methods=['POST'])
def predict():
    body = request.data.decode('utf-8')
    dataset = json.loads(body)
    new_data = []
    for d in dataset['questions']:
        new_data.append([d[3], d[4], d[10], d[11]])
    t_test = min_max_scaler_X.transform(np.array(new_data))
    pre = model.predict(t_test)
    resp = {'predictions': min_max_scaler_Y.inverse_transform(pre).tolist() }
    return jsonify(resp)

if __name__ == "__main__":
    app.debug = True
    app.run()