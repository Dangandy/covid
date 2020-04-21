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
    def get_data(self, country, model) -> np.array:
        """
        get last "7" days of data
        """
        # start date is 7 days ago
        start_date = datetime.now().date() + timedelta(days=-7)

        # get all prediction of country
        result = Stat.query.filter(Stat.date >= start_date).all()

        # create a map for each country and their 7 latest record
        memo = collections.defaultdict(list)
        for stat in result:
            memo[stat.country].append(stat.confirmed)

        countries = memo.keys()
        # its morning and I've been coding for 12 hours
        X = np.array([memo[country] for country in countries])
        X = X.reshape(X.shape[0], 1, X.shape[1])

        # predict
        y_pred = model.predict(X)

        # return in this format: [{'Canada', 'prediction'}]
        result = [
            {"country": country, "prediction": int(prediction)}
            for country, prediction in zip(countries, y_pred)
        ]
        print(result)


def main():
    """
    run code
    """
    # load model
    model = load_model("lstm_model.h5")
    p = Predict()
    p.get_data("Canada", model)

    # predict


if __name__ == "__main__":
    main()

