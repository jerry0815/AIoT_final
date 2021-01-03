import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from keras.layers import Dense
from keras.models import Sequential

df = pd.read_csv('./solar_data_202003_202007_processed.csv')
df = df[df['kwh']<30]


X = df[['HOUR','OPTPWR','IIT','IHT']]
Y = df[['kwh']]
min_max_scaler_X = MinMaxScaler()
min_max_scaler_Y = MinMaxScaler()
X_scale = min_max_scaler_X.fit_transform(X)
Y_scale = min_max_scaler_Y.fit_transform(Y)

X_train, X_test, y_train, y_test = train_test_split(
    X_scale, Y_scale, test_size=0.2, random_state=0
)

model = Sequential()
model.add(Dense(512, input_dim=4, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())

model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])

model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs = 100,
    batch_size = 128,
    verbose = 1
)

y_test_pred = model.predict(X_test)
r2 = r2_score(y_test, y_test_pred)
mse = mean_squared_error(y_test, y_test_pred)
print('MSE: %.3f, R^2: %.3f' % (mse, r2))

test = [[9, 15.8, 36, 41], [10, 7.55, 46, 41]]
t_test = min_max_scaler_X.transform(np.array(test))
pre = model.predict(t_test)
print(min_max_scaler_Y.inverse_transform(pre))

model.save('aiot.h5')