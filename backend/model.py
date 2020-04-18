#!/usr/bin/env python3
"""
Implementation of covid19 predictions using linear regression
"""
# imports
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle


class Model:
    def __init__(self):
        # variables
        self.url = "https://pomber.github.io/covid19/timeseries.json"
        self.model = None
        self.df = None

        # build
        self.build_df()
        self.build_model()

    def build_df(self) -> None:
        self.transform()
        self.preprocess_diff()
        self.preprocess_country()
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

        # return
        self.df = df

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

    def preprocess_country(self) -> None:
        dummies = pd.get_dummies(self.df.country)
        dummies["country"] = self.df.country
        dummies["date"] = self.df.date
        self.df = pd.merge(self.df, dummies, on=["country", "date"])

    def build_model(self) -> None:
        # get x columns
        x_columns = list(self.df.columns)
        x_columns.remove("confirmed")
        x_columns.remove("country")
        x_columns.remove("date")
        x_columns.remove("confirmed_diff")
        x_columns.remove("deaths")
        x_columns.remove("recovered")

        # get x y
        x = self.df[x_columns]
        y = self.df.confirmed_diff
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        # build model and save
        self.model = LinearRegression(fit_intercept=False).fit(x_train, y_train)
        pickle.dump(self.model, open("model.pkl", "wb"))


def main():
    """
    run code
    """
    Model()


if __name__ == "__main__":
    main()

