# -*- coding: utf-8 -*-
"""Testing: Predicting Electricity Generation of the Eastern Mid-Atlantic Region of the US.ipynb"""

#-----General------#
import numpy as np
import pandas as pd
import math
import random

#-----Plotting-----#
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#-----Utility-----#
import itertools
import warnings
warnings.filterwarnings("ignore")
from datetime import date, datetime
import json
import requests
import statsmodels.api as sm

if st.button('Refresh'):
    st.experimental_rerun()
else:
    st.write('Ready to Reload')



colUrl = 'https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key=klobKyhl5dK7WfbXBlMzFkpf3tD0TYakCzvXgsQ7&frequency=daily&data[0]=value&facets[fueltype][]=COL&facets[respondent][]=MIDA&facets[timezone][]=Eastern&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
r = requests.get(colUrl)
json_data = json.loads(r.text)

if r.status_code == 200:
    print('The Electricity Generation via Coal in the Eastern Region of The U.S. Mid-Atlantic:')
else:
    print('Error')

colDf = pd.DataFrame(json_data.get('response').get('data'))
colDf['period'] = pd.to_datetime(colDf['period'])

colDf = colDf.sort_values('period')
colDf.isnull().sum()

colDf = colDf.groupby('period')['value'].sum().reset_index()

colDf = colDf.set_index('period')
#colDf.index

col = colDf['value'].resample('MS').mean()

#colDf

"""

>**Past Data, Present Data, and Prediction of the Energy Generation via Coal in the Eastern Region of The U.S. Mid-Atlantic .**

"""

fig, ax = plt.subplots()
ax.plot(col)
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation via Coal in the Eastern Region of The U.S. Mid-Atlantic")
st.pyplot(fig)

decomposition = sm.tsa.seasonal_decompose(col, model='additive')
st.pyplot(decomposition.plot())

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(col,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue


mod = sm.tsa.statespace.SARIMAX(col,
                                order=(1, 0, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])


st.pyplot(results.plot_diagnostics())

pred = results.get_prediction(start=pd.to_datetime('2022-01-01'), dynamic=False)
pred_ci = pred.conf_int()
fig, ax = plt.subplots()
ax = col.plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("Accuracy Check for the Prediction for the Electricity Generation via Coal in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

col_forecasted = pred.predicted_mean
col_truth = col['2022-01-01':]
mse = ((col_forecasted - col_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
fig, ax = plt.subplots()
ax = col.plot(label='observed', figsize=(20, 10))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("The Prediction for the Electricity Generation via Coal in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

nucUrl = 'https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key=klobKyhl5dK7WfbXBlMzFkpf3tD0TYakCzvXgsQ7&frequency=daily&data[0]=value&facets[fueltype][]=NUC&facets[respondent][]=MIDA&facets[timezone][]=Eastern&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
r = requests.get(nucUrl)
json_data = json.loads(r.text)

if r.status_code == 200:
    print('The Electricity Generation via Nuclear in the Eastern Region of The U.S. Mid-Atlantic:')
else:
    print('Error')

nucDf = pd.DataFrame(json_data.get('response').get('data'))
nucDf['period'] = pd.to_datetime(nucDf['period'])

nucDf = nucDf.sort_values('period')
nucDf.isnull().sum()

nucDf = nucDf.groupby('period')['value'].sum().reset_index()

nucDf = nucDf.set_index('period')
#nucDf.index

nuc = nucDf['value'].resample('MS').mean()

#nucDf

"""

>**Past Data, Present Data, and Prediction of the Energy Generation via Nuclear in the Eastern Region of The U.S. Mid-Atlantic .**

"""

fig, ax = plt.subplots()
ax.plot(nuc)
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation via Nuclear in the Eastern Region of The U.S. Mid-Atlantic")
st.pyplot(fig)

decomposition = sm.tsa.seasonal_decompose(nuc['2018-10-01':], model='additive')

st.pyplot(decomposition.plot())

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(nuc['2018-10-01':],
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(nuc['2018-10-01':],
                                order=(1, 1, 0),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

st.pyplot(results.plot_diagnostics())

pred = results.get_prediction(start=pd.to_datetime('2022-01-01'), dynamic=False)
pred_ci = pred.conf_int()
fig, ax = plt.subplots()
ax = nuc['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("Accuracy Check for the Prediction for the Electricity Generation via Nuclear in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

nuc_forecasted = pred.predicted_mean
nuc_truth = nuc['2022-01-01':]
mse = ((nuc_forecasted - nuc_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
fig, ax = plt.subplots()
ax = nuc.plot(label='observed', figsize=(20, 10))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("The Prediction for the Electricity Generation via Nuclear in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

watUrl = 'https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key=klobKyhl5dK7WfbXBlMzFkpf3tD0TYakCzvXgsQ7&frequency=daily&data[0]=value&facets[fueltype][]=WAT&facets[respondent][]=MIDA&facets[timezone][]=Eastern&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
r = requests.get(watUrl)
json_data = json.loads(r.text)

if r.status_code == 200:
    print('The Electricity Generation via Water in the Eastern Region of The U.S. Mid-Atlantic:')
else:
    print('Error')

watDf = pd.DataFrame(json_data.get('response').get('data'))
watDf['period'] = pd.to_datetime(watDf['period'])

watDf = watDf.sort_values('period')
watDf.isnull().sum()

watDf = watDf.groupby('period')['value'].sum().reset_index()

watDf = watDf.set_index('period')
#watDf.index

wat = watDf['value'].resample('MS').mean()

#watDf

"""

>**Past Data, Present Data, and Prediction of the Energy Generation via Water in the Eastern Region of The U.S. Mid-Atlantic .**

"""

fig, ax = plt.subplots()
ax.plot(wat)
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation via Water in the Eastern Region of The U.S. Mid-Atlantic")
st.pyplot(fig)

decomposition = sm.tsa.seasonal_decompose(wat['2018-10-01':], model='additive')

st.pyplot(decomposition.plot())

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(wat['2018-10-01':],
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(wat['2018-10-01':],
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

st.pyplot(results.plot_diagnostics())

pred = results.get_prediction(start=pd.to_datetime('2022-01-01'), dynamic=False)
pred_ci = pred.conf_int()
fig, ax = plt.subplots()
ax = wat['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("Accuracy Check for the Prediction for the Electricty Generation via Water in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

wat_forecasted = pred.predicted_mean
wat_truth = wat['2022-01-01':]
mse = ((wat_forecasted - wat_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
fig, ax = plt.subplots()
ax = wat['2018':].plot(label='observed', figsize=(20, 10))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("The Prediction for the Electricty Generation via Water in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

ngUrl = 'https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key=klobKyhl5dK7WfbXBlMzFkpf3tD0TYakCzvXgsQ7&frequency=daily&data[0]=value&facets[fueltype][]=NG&facets[respondent][]=MIDA&facets[timezone][]=Eastern&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
r = requests.get(ngUrl)
json_data = json.loads(r.text)

if r.status_code == 200:
    print('The Electricity Generation via Natural Gas in the Eastern Region of The U.S. Mid-Atlantic:')
else:
    print('Error')

ngDf = pd.DataFrame(json_data.get('response').get('data'))
ngDf['period'] = pd.to_datetime(ngDf['period'])

ngDf = ngDf.sort_values('period')
ngDf.isnull().sum()

ngDf = ngDf.groupby('period')['value'].sum().reset_index()

ngDf = ngDf.set_index('period')
#ngDf.index

ng = ngDf['value'].resample('MS').mean()

#ngDf

"""

>**Past Data, Present Data, and Prediction of the Energy Generation via Natural Gas in the Eastern Region of The U.S. Mid-Atlantic**

"""

fig, ax = plt.subplots()
ax.plot(ng)
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation via Natural Gas in the Eastern Region of The U.S. Mid-Atlantic")
st.pyplot(fig)

decomposition = sm.tsa.seasonal_decompose(ng['2018-09-01':], model='additive')

st.pyplot(decomposition.plot())

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(ng['2018-09-01':],
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(ng['2018-09-01':],
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])


st.pyplot(results.plot_diagnostics())

pred = results.get_prediction(start=pd.to_datetime('2022-01-01'), dynamic=False)
pred_ci = pred.conf_int()
fig, ax = plt.subplots()
ax = ng['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("Accuracy Check for the Prediction for the Electricity Generation via Natural Gas in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

ng_forecasted = pred.predicted_mean
ng_truth = ng['2022-01-01':]
mse = ((ng_forecasted - ng_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
fig, ax = plt.subplots()
ax = ng['2018':].plot(label='observed', figsize=(20, 10))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("The Prediction for the Electrcity Generation via Natural Gas in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

oilUrl = 'https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key=klobKyhl5dK7WfbXBlMzFkpf3tD0TYakCzvXgsQ7&frequency=daily&data[0]=value&facets[fueltype][]=OIL&facets[respondent][]=MIDA&facets[timezone][]=Eastern&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
r = requests.get(oilUrl)
json_data = json.loads(r.text)

if r.status_code == 200:
    print('The Electricity Generation via Petroleum in the Eastern Region of The U.S. Mid-Atlantic:')
else:
    print('Error')

oilDf = pd.DataFrame(json_data.get('response').get('data'))
oilDf['period'] = pd.to_datetime(oilDf['period'])

oilDf = oilDf.sort_values('period')
oilDf.isnull().sum()

oilDf = oilDf.groupby('period')['value'].sum().reset_index()

oilDf = oilDf.set_index('period')
#oilDf.index

oil = oilDf['value'].resample('MS').mean()

#oilDf

"""

>**Past Data, Present Data, and Prediction of the Energy Generation via Petroleum in the Eastern Region of The U.S. Mid-Atlantic**

"""

fig, ax = plt.subplots()
ax.plot(oil)
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation via Petroleum in the Eastern Region of The U.S. Mid-Atlantic")
st.pyplot(fig)

decomposition = sm.tsa.seasonal_decompose(oil['2018-09-01':], model='additive')

st.pyplot(decomposition.plot())

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(oil['2018-09-01':],
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(oil['2018-09-01':],
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

st.pyplot(results.plot_diagnostics())

pred = results.get_prediction(start=pd.to_datetime('2022-01-01'), dynamic=False)
pred_ci = pred.conf_int()
fig, ax = plt.subplots()
ax = oil['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("Accuracy Check for the Prediction for the Electricity Generation via Petroleum in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

oil_forecasted = pred.predicted_mean
oil_truth = oil['2022-01-01':]
mse = ((oil_forecasted - oil_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
fig, ax = plt.subplots()
ax = oil['2018':].plot(label='observed', figsize=(20, 10))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("The Prediction for the Electrcity Generation via Petroleum in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

sunUrl = 'https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key=klobKyhl5dK7WfbXBlMzFkpf3tD0TYakCzvXgsQ7&frequency=daily&data[0]=value&facets[fueltype][]=SUN&facets[respondent][]=MIDA&facets[timezone][]=Eastern&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
r = requests.get(sunUrl)
json_data = json.loads(r.text)

if r.status_code == 200:
    print('The Electricity Generation via Solar in the Eastern Region of The U.S. Mid-Atlantic:')
else:
    print('Error')

sunDf = pd.DataFrame(json_data.get('response').get('data'))
sunDf['period'] = pd.to_datetime(sunDf['period'])

sunDf = sunDf.sort_values('period')
sunDf.isnull().sum()

sunDf = sunDf.groupby('period')['value'].sum().reset_index()

sunDf = sunDf.set_index('period')
#sunDf.index

sun = sunDf['value'].resample('MS').mean()

#sunDf

"""

>**Past Data, Present Data, and Prediction of the Energy Generation via Solar in the Eastern Region of The U.S. Mid-Atlantic**

"""

fig, ax = plt.subplots()
ax.plot(sun)
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation via Solar in the Eastern Region of The U.S. Mid-Atlantic")
st.pyplot(fig)

decomposition = sm.tsa.seasonal_decompose(sun['2018-09-01':], model='additive')

st.pyplot(decomposition.plot())

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(sun['2018-09-01':],
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(sun['2018-09-01':],
                                order=(1, 1, 0),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

st.pyplot(results.plot_diagnostics())

pred = results.get_prediction(start=pd.to_datetime('2022-01-01'), dynamic=False)
pred_ci = pred.conf_int()
fig, ax = plt.subplots()
ax = sun['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("Accuracy Check for the Prediction for the Electricity Generation via Solar in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

sun_forecasted = pred.predicted_mean
sun_truth = sun['2022-01-01':]
mse = ((sun_forecasted - sun_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
fig, ax = plt.subplots()
ax = sun.plot(label='observed', figsize=(20, 10))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("The Prediction for the Electrcity Generation via Solar in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

wndUrl = 'https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key=klobKyhl5dK7WfbXBlMzFkpf3tD0TYakCzvXgsQ7&frequency=daily&data[0]=value&facets[fueltype][]=WND&facets[respondent][]=MIDA&facets[timezone][]=Eastern&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
r = requests.get(wndUrl)
json_data = json.loads(r.text)

if r.status_code == 200:
    print('The Electricity Generation via Wind in the Eastern Region of The U.S. Mid-Atlantic:')
else:
    print('Error')

wndDf = pd.DataFrame(json_data.get('response').get('data'))
wndDf['period'] = pd.to_datetime(wndDf['period'])

wndDf = wndDf.sort_values('period')
wndDf.isnull().sum()

wndDf = wndDf.groupby('period')['value'].sum().reset_index()

wndDf = wndDf.set_index('period')
#wndDf.index

wnd = wndDf['value'].resample('MS').mean()

#wndDf

"""

>**Past Data, Present Data, and Prediction of the Energy Generation via Wind in the Eastern Region of The U.S. Mid-Atlantic**

"""

fig, ax = plt.subplots()
ax.plot(wnd)
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation via Wind in the Eastern Region of The U.S. Mid-Atlantic")
st.pyplot(fig)

decomposition = sm.tsa.seasonal_decompose(wnd['2018-09-01':], model='additive')

st.pyplot(decomposition.plot())

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(wnd['2018-09-01':],
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(wnd['2018-09-01':],
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

st.pyplot(results.plot_diagnostics())

pred = results.get_prediction(start=pd.to_datetime('2022-01-01'), dynamic=False)
pred_ci = pred.conf_int()
fig, ax = plt.subplots()
ax = wnd['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("Accuracy Check for the Prediction for the Electricity Generation via Wind in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

wnd_forecasted = pred.predicted_mean
wnd_truth = wnd['2022-01-01':]
mse = ((wnd_forecasted - wnd_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
fig, ax = plt.subplots()
ax = wnd.plot(label='observed', figsize=(20, 10))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("The Prediction for the Electrcity Generation via Wind in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

othUrl = 'https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key=klobKyhl5dK7WfbXBlMzFkpf3tD0TYakCzvXgsQ7&frequency=daily&data[0]=value&facets[fueltype][]=OTH&facets[respondent][]=MIDA&facets[timezone][]=Eastern&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
r = requests.get(othUrl)
json_data = json.loads(r.text)

if r.status_code == 200:
    print('The Electricity Generation via Other Energy Sources in the Eastern Region of The U.S. Mid-Atlantic:')
else:
    print('Error')

othDf = pd.DataFrame(json_data.get('response').get('data'))
othDf['period'] = pd.to_datetime(othDf['period'])

othDf = othDf.sort_values('period')
othDf.isnull().sum()

othDf = othDf.groupby('period')['value'].sum().reset_index()

othDf = othDf.set_index('period')
#othDf.index

oth = othDf['value'].resample('MS').mean()

#othDf

"""

>**Past Data, Present Data, and Prediction of the Energy Generation via Other Energy Sources in the Eastern Region of The U.S. Mid-Atlantic**

"""

fig, ax = plt.subplots()
ax.plot(oth)
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation via Other Energy Sources in the Eastern Region of The U.S. Mid-Atlantic")
st.pyplot(fig)

decomposition = sm.tsa.seasonal_decompose(oth['2018-09-01':], model='additive')

st.pyplot(decomposition.plot())

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(oth['2018-09-01':],
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(oth['2018-09-01':],
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

st.pyplot(results.plot_diagnostics())

pred = results.get_prediction(start=pd.to_datetime('2022-01-01'), dynamic=False)
pred_ci = pred.conf_int()
fig, ax = plt.subplots()
ax = oth['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("Accuracy Check for the Prediction for the Electricity Generation via Other Energy Sources in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

oth_forecasted = pred.predicted_mean
oth_truth = oth['2022-01-01':]
mse = ((oth_forecasted - oth_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

pred_uc = results.get_forecast(steps=100)
pred_ci = pred_uc.conf_int()
fig, ax = plt.subplots()
ax = oth.plot(label='observed', figsize=(20, 10))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Electricity Generated (Megawatthours)')
plt.title("The Prediction for the Electrcity Generation via Other Enegry Sources in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)

"""

>**Past and Present Data of the Energy Generation in the Eastern Region of The U.S. Mid-Atlantic**

"""

fig, ax = plt.subplots()
ax.plot(col, label = 'Coal')
ax.plot(nuc, label = 'Nuclear')
ax.plot(wat, label = 'Hydro')
ax.plot(ng, label = 'Natural Gas')
ax.plot(oil, label = 'Petroleum')
ax.plot(sun, label = 'Solar')
ax.plot(wnd, label = 'Wind')
ax.plot(oth, label = 'Other Engery Sources')
ax.grid()
ax.set_xlabel("Years (YYYY-MM-DD)")
ax.set_ylabel("Electricity Generated (Megawatthours)")
plt.title("The Electricity Generation in the Eastern Region of The U.S. Mid-Atlantic")
plt.legend()
st.pyplot(fig)