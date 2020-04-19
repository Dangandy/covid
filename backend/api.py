# server stuff
from flask import Flask
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

from keras.models import load_model


# start server
app = Flask(__name__)
app.debug = True

model = load_model("lstm_model.h5")
df = pd.read_csv("df.csv", parse_dates=["date"])
countries = list(df["country"].unique())
forecast_date = df["date"].max()
win_size = 7

def build_latest_set(df,  metric):
   # forecast_date = forecast_date.strftime("%Y-%m-%d")
    raw = df.query("date<'{0}'".format(forecast_date))
    
    x = []
  
    for country in countries:
        temp = raw[raw["country"]==country]
        series = temp[metric]
        x.append(series[len(series)-win_size:len(series)+1])
    return np.array(x)

def forecast(model, data, start_date, num_days, win_size=7):
    result_=dict()
    for i in range(len(data)):
        result_[i]=[]
    y_pred=model.predict(data)

    dates=[]
    #date_temp = pd.datetime.strptime(start_date, "%Y-%m-%d")
    date_temp = start_date
    for j in range(1,num_days+1):
        for i in range(len(data)): # This loops for each country
            cur_window=list(data[i][0][1:win_size+1])
            result_[i].append(cur_window[-1])
            cur_window.append(y_pred[i])
            data[i][0]=cur_window
        y_pred=model.predict(data)
        dates.append(date_temp.strftime("%Y-%m-%d"))
        date_temp+=relativedelta(days=1)
    result=pd.DataFrame(pd.DataFrame(pd.DataFrame(result_).values.T)) 
    result.columns=dates
    result['country']=countries
    return result

def extract_country_predict(predict, metric, country):
    temp = predict[predict["country"] == country]

    temp = temp.drop(columns="country").T
    temp.reset_index(inplace=True)
    #Drop the first row
    temp.drop([0], inplace=True)
    #Rename column to metric
    temp.columns = ["date", "prediction" ]
    return temp


@app.route("/api/predict/<country>")
def predict(country):
    """
    predicts the countrys confirmed cases tomorrow.. country must be capital ☹️
    """
    metric = "confirmed"
    latest = build_latest_set(df,  metric)

    # Reshape for LSTM model
    latest = latest.reshape(latest.shape[0], 1, 
                            latest.shape[1])
    #
    # pred 5!!
    forecast_set = forecast(model, latest, forecast_date, 5, win_size)
    #print(forecast_set)
    #Extract specific country
    last_df = extract_country_predict(forecast_set, metric, country)
    #last_df["date"] = pd.to_datetime(last_df["date"])
    
    #last_df.date_counter = last_df.date_counter.apply(lambda x: x + 10)
    #X_test = last_df[X_columns]
    """
    results = [
        {
            "date": last_df.iloc[i, :]["date"],
            "prediction": last_df.iloc[-1, :]["confirmed"] + sum(y_pred[: i + 1]),
        }
        for i, pred in enumerate(y_pred)
    ]
    """
    results = last_df.to_dict(orient="records")
   # print(results)
    return {"results": results}, 200


@app.route("/api/plot/<country>")
def plot(country):
    """
    pulls all the date and confirmed from the df and return the data for that specific country
    """
    country_df = df[df.country == country]
    dates = list(country_df["date"].astype(str))
    confirmed = list(country_df["confirmed"].astype(int))

    # build object
    array = [{"date": dates[i], "confirmed": confirmed[i]} for i in range(len(dates))]
    return {"results": array}, 200


@app.route("/api/stats/World")
def worldStats():
    """
    get sum of all stats
    """
    return (
        {
            "confirmed": int(sum(df.confirmed_diff)),
            "deaths": int(sum(df.deaths_diff)),
            "recovered": int(sum(df.recovered_diff)),
        },
        200,
    )


@app.route("/api/stats/<country>")
def stats(country):
    """
    grab the total confirmed, deaths, and recovered cases for the country
    """
    country_df = df[df.country == country]
    confirmed = country_df["confirmed"].max()
    deaths = country_df["deaths"].max()
    recovered = country_df["recovered"].max()
    return (
        {
            "confirmed": int(confirmed),
            "deaths": int(deaths),
            "recovered": int(recovered),
        },
        200,
    )

#if __name__ == "__main__":
#    predict("Canada")




