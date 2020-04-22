#!/usr/bin/env python3
"""
Predict upcoming confirmed cases using LSTM model
"""
# import
from keras.models import load_model
import numpy as np
from datetime import datetime, timedelta
import collections

# local import
from db.model import db, Stat


class Predict:
    def __init__(self):
        # start date is 7 days ago
        self.today = datetime.now().date()
        self.start_date = self.today + timedelta(days=-7)

    def get_data(self):
        """
        get last "7" days of data
        """
        # get all prediction of country
        result = Stat.query.filter(
            Stat.date >= self.start_date, Stat.date < self.today
        ).all()

        # create a map for each country and their 7 latest record
        memo = collections.defaultdict(list)
        for stat in result:
            memo[stat.country].append(stat.confirmed)

        # return
        countries = memo.keys()
        X = np.array([memo[country] for country in countries])
        X = X.reshape(X.shape[0], 1, X.shape[1])
        return countries, X

    def predict(self, countries, X, model):
        """
        predict, then predict again
        """
        # variables
        data = []

        # predict - we'll be shifting x every iteration because predict output 1 value
        for i in range(7):
            _X = np.array([x[i : 7 + i] for [x] in X])
            _X = _X.reshape(_X.shape[0], 1, _X.shape[1])
            y_pred = model.predict(_X)

            # add new prediction to x
            X = np.array([np.append(x, y_pred[j]) for j, [x] in enumerate(X)])
            X = X.reshape(X.shape[0], 1, X.shape[1])

        # add predictions into database..
        y_pred = [x[7:14] for [x] in X]
        for country, prediction in zip(countries, y_pred):
            for i, pred in enumerate(prediction):
                pred_date = self.today + timedelta(days=i)
                data.append(
                    Stat(
                        id=f"{country}{pred_date}",
                        country=country,
                        date=pred_date,
                        confirmed_pred=int(pred),
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
                query.confirmed = stat.confirmed
                query.deaths = stat.deaths
                query.recovered = stat.recovered
                query.confirmed_pred = (
                    stat.confirmed_pred if stat.confirmed_pred else None
                )
                query.deaths_pred = stat.deaths_pred if stat.deaths_pred else None
                query.recovered_pred = (
                    stat.recovered_pred if stat.recovered_pred else None
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
    countries, X = predict.get_data()
    data = predict.predict(countries, X, lstm)

    # save to db
    predict.load(data)


if __name__ == "__main__":
    main()

