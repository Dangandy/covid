from model import db, Stat
import requests


class Create:
    def __init__(self):
        # variables
        self.url = "https://pomber.github.io/covid19/timeseries.json"

    def extract(self):
        # get json data
        response = requests.get(self.url)
        json = response.json()

        # return
        return json

    def transform(self, json: dict):
        # variables
        countries = json.keys()
        all_data = []

        # loop
        for country in countries:

            # build array of json
            for i, stat in enumerate(json[country]):
                data = Stat(
                    id=f"{country}{stat['date']}",
                    country=country,
                    date=stat["date"],
                    confirmed=stat["confirmed"],
                    deaths=stat["deaths"],
                    recovered=stat["recovered"],
                )
                all_data.append(data)

        # return
        return all_data

    def load(self, data):
        # create db
        db.create_all()

        # add to db
        db.session.bulk_save_objects(data)
        db.session.commit()


def main():
    """
    1. Extract JSON from url
    2. Transform JSON into: id, country, confirmed, recovered, deaths
        - id is in the form of {country}{date}
    3. Load object into sqlite database
    """
    create = Create()
    json = create.extract()
    data = create.transform(json)
    create.load(data)


if __name__ == "__main__":
    main()
