import numpy as np
import csv
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt

def rmse(y, y_pred):
	return np.sqrt(np.mean(np.square(y - y_pred)))

df = pd.read_csv("1c_actual.csv", usecols = ['premium'])
x = df.as_matrix()
actual_data = x.astype(np.float)
print(actual_data)

df = pd.read_csv("file1c_output.csv", usecols = ['new_premium'])
x = df.as_matrix()
estimated_data = x.astype(np.float)
print(estimated_data)

rmse = sqrt(mean_squared_error(actual_data, estimated_data))
print(rmse)
