#!/usr/bin/env python3
"""
Predict upcoming confirmed cases using LSTM model
"""
# import
from keras.models import load_model
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import collections

# local import
from db.model import db, Stat

# global variables?
DELTA = 10
today = datetime.now().date()
start_date = today + timedelta(days=-DELTA)


class Predict:
    def get_data(self):
        """
        get last "7" days of data by storing sql statement into dataframe and transforming it
        """
        # get all prediction of country
        df = pd.read_sql(
            Stat.query.filter(Stat.date >= start_date, Stat.date < today).statement,
            db.session.bind,
        )

        # transform df
        df.sort_values(by=["country", "date"], inplace=True)
        df["confirmed_diff"] = np.where(
            df.country == df.country.shift(), df.confirmed - df.confirmed.shift(), 0
        )
        last7_df = df.groupby("country").tail(7)
        last1_df = df.groupby("country").tail(1)

        # get key variables from df
        num_countries = df.country.nunique()
        X = np.array(last7_df.confirmed_diff)
        X = X.reshape(num_countries, 1, 7)

        countries = last1_df.country
        confirmed = last1_df.confirmed
        last_date = max(last1_df.date)

        # return
        return X, countries, confirmed, last_date

    def predict(self, X, countries, confirmed, last_date, model):
        """
        predict, then predict again
        """
        # variables
        data = []
        countries_zip = zip(countries, confirmed)

        # predict - we'll be shifting x every iteration because predict output 1 value
        for i in range(7):
            _X = np.array([x[-7:] for [x] in X])
            _X = _X.reshape(_X.shape[0], 1, _X.shape[1])
            y_pred = model.predict(_X)

            # add new prediction to x
            X = np.array([np.append(x, y_pred[j]) for j, [x] in enumerate(X)])
            X = X.reshape(X.shape[0], 1, X.shape[1])

        # add predictions into database..
        y_pred = [x[-7:] for [x] in X]
        for (country, confirm), prediction in zip(countries_zip, y_pred):
            total = confirm
            for i, pred in enumerate(prediction):
                total += pred
                pred_date = last_date + timedelta(days=i + 1)
                data.append(
                    Stat(
                        id=f"{country}{pred_date}",
                        country=country,
                        date=pred_date,
                        confirmed_pred=int(total),
                    )
                )

        # return
        return data

    def load(self, data):
        """
        insert if doesn't exist, update otherwise
        """
        # loop
        for stat in data:
            query = Stat.query.get({"id": stat.id})
            if query:
                query.confirmed_pred = (
                    stat.confirmed_pred if stat.confirmed_pred else None
                )
            else:
                db.session.add(stat)

        # commit
        db.session.commit()


def main():
    """
    run code
    """
    # variables
    predict = Predict()

    # load model
    lstm = load_model("lstm_model.h5")
    X, countries, confirmed, last_date = predict.get_data()
    data = predict.predict(X, countries, confirmed, last_date, lstm)

    # save to db
    predict.load(data)


if __name__ == "__main__":
    main()

