#!/usr/bin/env python3
"""
testing the implementation with the sqlite
"""
# 3rd party imports
from flask import Flask
from datetime import datetime, timedelta

# local imports
from db.model import db, Stat, app


@app.route("/api/stats/<country>")
def stats(country):
    """
    SQL Statement:
        select * from stat where stat.confirmed is not null and stat.country = <country> order by stat.date desc limit 1;
    """
    # search db
    result = (
        Stat.query.filter(Stat.confirmed != None, Stat.country == country)
        .order_by(Stat.date.desc())
        .first()
    )

    # return
    return (
        {
            "confirmed": result.confirmed,
            "deaths": result.deaths,
            "recovered": result.recovered,
        },
        200,
    )


@app.route("/api/stats/World")
def worldStats():
    """
    grab all records from today ( or latest record.. )
    """
    # search db
    confirmed, recovered, deaths = (
        db.session.query(
            db.func.sum(Stat.confirmed),
            db.func.sum(Stat.recovered),
            db.func.sum(Stat.deaths),
        )
        .filter(Stat.confirmed != None)
        .order_by(Stat.date.desc())
        .limit(1)
        .first()
    )

    # return
    return {"confirmed": confirmed, "recovered": recovered, "deaths": deaths}, 200


@app.route("/api/plot/<country>")
def history(country):
    """
    pull all historic data on country
    """
    # varialbes
    array = []

    # use filter to get all data
    result = Stat.query.filter_by(country=country).all()

    # build array
    for record in result:
        array.append(
            {
                "confirmed": record.confirmed,
                "date": record.date,
                "recovered": record.recovered,
                "deaths": record.deaths,
                "confirmed_pred": record.confirmed_pred,
            }
        )

    # return
    return {"result": array}, 200


if __name__ == "__main__":
    # app.debug = True
    app.run()
