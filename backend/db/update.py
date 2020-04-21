#!/usr/bin/env python3
"""
Implementation of updating sqlite db
"""
from datetime import datetime
from model import db, Stat
from create import Create


class Update(Create):
    def transform(self, json: dict):
        # variables
        countries = json.keys()
        all_data = []
        last_days = []

        # loop
        for country in countries:

            # build array of json
            for i, stat in enumerate(json[country]):
                data = Stat(
                    id=f"{country}{stat['date']}",
                    country=country,
                    date=datetime.strptime(stat["date"], "%Y-%m-%d").date(),
                    confirmed=stat["confirmed"],
                    deaths=stat["deaths"],
                    recovered=stat["recovered"],
                )
                all_data.append(data)

            # get today and yesterday's data
            today = data
            yesterday_stats = json[country][i - 1]
            yesterday = Stat(
                id=f"{country}{yesterday_stats['date']}",
                country=country,
                date=datetime.strptime(yesterday_stats["date"], "%Y-%m-%d").date(),
                confirmed=yesterday_stats["confirmed"],
                deaths=yesterday_stats["deaths"],
                recovered=yesterday_stats["recovered"],
            )

            last_days.append(today)
            last_days.append(yesterday)

        # return
        return all_data, last_days

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
            else:
                db.session.add(stat)

        # commit
        db.session.commit()


def main():
    """
    1. Extract new data from url
    2. get last 2 days data ( data here is updated hourly )
    3. insert / update into db
    """
    update = Update()
    json = update.extract()
    _, last_days = update.transform(json)
    update.load(last_days)


if __name__ == "__main__":
    main()

