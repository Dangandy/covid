#!/usr/bin/env python3
"""
Implementation of building LSTM model
"""
# 3rd party imports
import pandas as pd
import numpy as np
import random as rn
import datetime as datetime

# model
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.losses import MeanSquaredLogarithmicError
from sklearn.model_selection import train_test_split

# local imports
from db.model import db, Stat


class Lstm:
    def extract(self) -> pd.DataFrame:
        """
        extract data from database and output into dataframe
        """
        # grab all record from stat table
        df = pd.read_sql_table("stat", "sqlite:///db/site.db")

        # return
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        transforms done to dataframe:
        - calculate the difference of each metric
        - onehotencode countries
        """
        # get diff
        df["confirmed_diff"] = np.where(
            df.country == df.country.shift(), df.confirmed - df.confirmed.shift(), 0
        )
        df["recovered_diff"] = np.where(
            df.country == df.country.shift(), df.recovered - df.recovered.shift(), 0
        )
        df["deaths_diff"] = np.where(
            df.country == df.country.shift(), df.deaths - df.deaths.shift(), 0
        )

        # encode country with pd.dummies
        dummies = pd.get_dummies(df.country)
        dummies["id"] = df.id
        df = pd.merge(df, dummies, on=["id"])

        # return
        return df

    def load(
        self,
        df: pd.DataFrame,
        metric="confirmed",
        win_size=7,
        epochs=5,
        batch_size=32,
        save=False,
    ) -> Sequential:
        """
        load dataframe into sequential
        """
        # variables
        x, y = [], []
        countries = db.session.query(Stat.country).distinct().all()

        # countries come in the form of [('Afghanistan',), ('Albania',), ... ]
        for (country,) in countries:
            country_df = df[df.country == country]
            series = list(country_df[metric])
            for i in range(0, len(series) - win_size):
                end = i + win_size
                series_x, series_y = series[i:end], series[end]
                if series_y:
                    x.append(series_x)
                    y.append(series_y)
        X, y = np.array(x), np.array(y)

        # TTS
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # preprocess
        X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
        X_val = X_val.reshape(X_val.shape[0], 1, X_val.shape[1])

        # build model
        model = Sequential()
        model.add(
            LSTM(
                100,
                activation="relu",
                input_shape=(1, win_size),
                return_sequences=True,
            )
        )
        model.add(LSTM(150, activation="relu"))
        model.add(Dense(1, activation="relu"))

        # Compile Model
        model.compile(optimizer="adam", loss=MeanSquaredLogarithmicError())

        # Fit Model
        model.fit(
            X_train,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_val, y_val),
            verbose=2,
            shuffle=True,
        )

        # Export Model
        if save:
            model.save("lstm_model.h5")


def main():
    """
    run code
    """
    # Set random state for Keras
    np.random.seed(42)
    rn.seed(12345)
    tf.random.set_seed(1234)

    # build model and save it
    model = Lstm()
    df = model.extract()
    df = model.transform(df)
    lstm = model.load(df, save=True)


if __name__ == "__main__":
    main()

