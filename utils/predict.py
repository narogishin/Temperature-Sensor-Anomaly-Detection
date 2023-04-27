import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMAResults
import pandas as pd

data = pd.read_csv('utils/data.csv', index_col = 0)
Temperature = data['Tempreture']
Humidity = data['Humidity']

# loaded = ARIMAResults.load("model.pkl")

Temperature_model = sm.tsa.ARIMA(Temperature, order=(1,0,1))
Temperature_model_fit = Temperature_model.fit()

Humidity_model = sm.tsa.ARIMA(Humidity, order=(2,1,2))
Humidity_model_fit = Humidity_model.fit()

def Temperature_forecast(t):
    return float(Temperature_model_fit.predict(start=t, end=t))

def Humidity_forecast(t):
    return float(Humidity_model_fit.predict(start=t, end=t))