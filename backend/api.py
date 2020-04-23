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
def worldTotal():
    """
    grab all records from today ( or latest record.. )
    """
    # search db
    result = (
        db.session.query(
            db.func.max(Stat.confirmed).label("confirmed"),
            db.func.max(Stat.recovered).label("recovered"),
            db.func.max(Stat.deaths).label("deaths"),
        )
        .filter(Stat.confirmed != None)
        .order_by(Stat.date.desc())
        .group_by(Stat.country)
        .all()
    )

    # get sums because I don't know how to do it in SQLAlchemy..
    confirmed = sum(r[0] for r in result)
    recovered = sum(r[1] for r in result)
    deaths = sum(r[2] for r in result)

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


@app.route("/api/plot/World")
def worldStats():
    """
    grab all stats of last updated date
    """
    # variables
    array = []

    # query
    result = (
        db.session.query(
            Stat.country,
            db.func.max(Stat.confirmed).label("confirmed"),
            Stat.recovered,
            Stat.deaths,
            Stat.confirmed_pred,
        )
        .group_by(Stat.country)
        .all()
    )

    # build array
    for record in result:
        array.append(
            {
                "country": record.country,
                "confirmed": record.confirmed,
                "recovered": record.recovered,
                "deaths": record.deaths,
                "confirmed_pred": record.confirmed_pred,
            }
        )

    # return
    return {"result": array}, 200


if __name__ == "__main__":
    app.debug = True
    app.run()
