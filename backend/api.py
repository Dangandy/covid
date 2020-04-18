# server stuff
from flask import Flask
import pickle
import pandas as pd

# start server
app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
df = pd.read_csv("df.csv")


@app.route("/api/predict/<country>")
def predict(country):
    """
    predicts the countrys confirmed cases tomorrow.. country must be capital ☹️
    """
    # variables
    X_columns = list(df.columns)
    X_columns.remove("confirmed")
    X_columns.remove("country")
    X_columns.remove("date")
    X_columns.remove("confirmed_diff")
    X_columns.remove("deaths")
    X_columns.remove("recovered")

    # pred 10!!
    last_df = df[df.country == country].tail(10)
    last_df["date"] = pd.to_datetime(last_df["date"])
    last_df["date"] = last_df["date"] + pd.DateOffset(days=10)
    last_df.date_counter = last_df.date_counter.apply(lambda x: x + 10)
    X_test = last_df[X_columns]
    y_pred = model.predict(X_test)
    results = [
        {
            "date": last_df.iloc[i, :]["date"],
            "prediction": last_df.iloc[-1, :]["confirmed"] + sum(y_pred[: i + 1]),
        }
        for i, pred in enumerate(y_pred)
    ]
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


@app.route("/api/stats/World")
def worldStats():
    """
    get sum of all stats
    """
    last_date_df = df.sort_values(by="date").drop_duplicates(
        subset="country", keep="last"
    )
    confirmed = sum(last_date_df.confirmed)
    deaths = sum(last_date_df.deaths)
    recovered = sum(last_date_df.recovered)
    return (
        {
            "confirmed": int(confirmed),
            "deaths": int(deaths),
            "recovered": int(recovered),
        },
        200,
    )
