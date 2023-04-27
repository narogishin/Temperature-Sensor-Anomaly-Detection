import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scalecast.Forecaster import Forecaster
sns.set(rc={'figure.figsize':(15,8)})


data = pd.read_csv('data.csv')

pd.to_datetime(data['Time'], unit='s')

f = Forecaster(y=data['Tempreture'],
                   current_dates=data['Time'])

f.manual_forecast(call_me='lstm_default')
f.plot_test_set(ci=True)