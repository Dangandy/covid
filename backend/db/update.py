#!/usr/bin/env python3
"""
Implementation of updating sqlite db
"""
from datetime import datetime, timedelta

from create import Create, db, Stat


class Update(Create):
    def transform(self, json: dict):
        # variables
        countries = json.keys()
        update_data = []

        # we only want to update everything from yesterday onwards..
        update_day = datetime.now().date() + timedelta(days=-7)

        # loop and build array of Stat
        for country in countries:
            for i, stat in enumerate(json[country]):
                date = datetime.strptime(stat["date"], "%Y-%m-%d").date()

                if date >= update_day:
                    update_data.append(
                        Stat(
                            id=f"{country}{date}",
                            country=country,
                            date=date,
                            confirmed=stat["confirmed"],
                            deaths=stat["deaths"],
                            recovered=stat["recovered"],
                        )
                    )

        # return
        return update_data

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
    last_days = update.transform(json)
    update.load(last_days)


if __name__ == "__main__":
    main()
