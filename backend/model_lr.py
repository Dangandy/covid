#!/usr/bin/env python3
"""
Implementation of covid19 predictions using linear regression
"""
# imports
import requests
import pandas as pd
import numpy as np
import random as rn
import tensorflow as tf

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.losses import MeanSquaredLogarithmicError
from sklearn.model_selection import train_test_split

# Set random state for Keras
np.random.seed(42)
rn.seed(12345)
tf.random.set_seed(1234)



class Model:
    def __init__(self):
        # variables
        self.url = "https://pomber.github.io/covid19/timeseries.json"
        self.model = None
        self.df = None
        self.countries = None
        self.forecast_start_date = None
        
        # Model variables
        self.x_train = None
        self.x_val = None
        self.y_train = None
        self.y_val = None
        self.n_feats = 1
        self.win_size = 7

        # LSTM parameters
        self.epochs = 5
        self.batch_size = 32
        

        # build
        self.build_df()
        self.build_model()

    def build_df(self) -> None:
        self.transform()
        self.preprocess_diff()
        
        self.df.to_csv("df.csv", index=False)

    def transform(self) -> None:
        # get json data
        response = requests.get(self.url)
        json = response.json()

        # transform json to dataframe
        countries = json.keys()
        df_array = []
        for country in countries:
            stats = json[country]
            for stat in stats:
                # build row
                date = stat["date"]
                confirmed = stat["confirmed"]
                deaths = stat["deaths"]
                recovered = stat["recovered"]
                df_array.append([country, date, confirmed, deaths, recovered])
        df = pd.DataFrame(df_array)
        df.columns = ["country", "date", "confirmed", "deaths", "recovered"]
        df["date"] = pd.to_datetime(df["date"])

        # return
        self.df = df
        self.countries = countries
        forecast_start_date = df["date"].max()
        self.forecast_start_date = forecast_start_date.strftime("%Y-%m-%d")
        print(self.forecast_start_date)

    def preprocess_diff(self) -> None:
        # variables
        current_country = ""
        current_count = 0
        confirmed_prev = 0
        confirmed_diff = 0
        deaths_prev = 0
        deaths_diff = 0
        recovered_prev = 0
        recovered_diff = 0
        date_counter = []
        confirmed_diff_array = []
        recovered_array = []
        deaths_array = []

        # loop
        for i in range(self.df.shape[0]):
            # reset
            if current_country != self.df.iloc[i, :].country:
                current_country = self.df.iloc[i, :].country
                current_count = 0
                confirmed_diff = 0
                confirmed_prev = 0
                deaths_prev = 0
                deaths_diff = 0
                recovered_prev = 0
                recovered_diff = 0

            else:
                # check if the previous date's confirmed is not 0
                if self.df.iloc[i, :].confirmed != 0:
                    current_count += 1
                    confirmed_diff = self.df.iloc[i, :].confirmed - confirmed_prev
                    confirmed_prev = self.df.iloc[i, :].confirmed
                    deaths_diff = self.df.iloc[i, :].deaths - deaths_prev
                    deaths_prev = self.df.iloc[i, :].deaths
                    recovered_diff = self.df.iloc[i, :].recovered - recovered_prev
                    recovered_prev = self.df.iloc[i, :].recovered

            # add to arrays
            date_counter.append(current_count)
            confirmed_diff_array.append(confirmed_diff)
            recovered_array.append(recovered_diff)
            deaths_array.append(deaths_diff)

        # add to df
        self.df["date_counter"] = date_counter
        self.df["confirmed_diff"] = confirmed_diff_array
        self.df["recovered_diff"] = recovered_array
        self.df["deaths_diff"] = deaths_array
    
    def build_train_data(self, metric):
        # Extract data only before pivot_date
        temp_df = self.df.query("date<'{0}'".format(self.forecast_start_date))
        win_size = self.win_size

        x=[]
        y=[]

        # Extract data before forecast_start_date
        for country in self.countries:
            temp = temp_df[temp_df["country"] == country]
            series = list(temp[metric])
            for i in range(len(series)): # Convert series to supervised
                end = i + win_size
                if end > len(series) -1:
                    break
                series_x, series_y = series[i:end], series[end]
                if (series_y != 0):
                    x.append(series_x)
                    y.append(series_y)
        return np.array(x), np.array(y)
         

        print(self.forecast_start_date)

    def train_model(self) -> None:
        model = Sequential()
        model.add(LSTM(100, activation="relu", 
            input_shape=(self.n_feats, self.win_size), 
            return_sequences=True))
        model.add(LSTM(150, activation="relu"))
        model.add(Dense(1, activation="relu"))
        #model.summary()
        
        # Compile Model
        model.compile(optimizer='adam', loss=MeanSquaredLogarithmicError())
        
        # Fit Model
        model.fit(self.x_train, self.y_train, epochs = self.epochs,
                batch_size = self.batch_size, 
                validation_data = (self.x_val, self.y_val), 
                verbose = 2,
                shuffle = True
        )

<<<<<<< HEAD:backend/model.py
        # Export Model
        model.save("lstm_model.h5")
=======
    def preprocess_country(self) -> None:
        dummies = pd.get_dummies(self.df.country)
        dummies["country"] = self.df.country
        dummies["date"] = self.df.date
        df = pd.merge(self.df, dummies, on=["country", "date"])
        self.df = df
>>>>>>> 1c443407492bdc3a83b85286821ab2bcfaa24bb1:backend/model_lr.py

    def build_train_val_sets(self, metric) -> None:
        x, y = self.build_train_data(metric)
        
        # Split between train and validation
        x_train, x_val, y_train, y_val = train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        # Reshape for LSTM NN
        self.x_train = x_train.reshape((x_train.shape[0], self.n_feats, x_train.shape[1]))
        self.x_val = x_val.reshape((x_val.shape[0], self.n_feats, x_val.shape[1]))
        
        self.y_train = y_train
        self.y_val = y_val


      
    def build_model(self) -> None:
        self.build_train_val_sets("confirmed")

        # build model and save
        self.train_model() 


def main():
    """
    run code
    """
    Model()


if __name__ == "__main__":
    main()

