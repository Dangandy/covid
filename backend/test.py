#!/usr/bin/env python3
"""
testing the implementation with the sqlite
"""
# 3rd party imports
from flask import Flask
from datetime import datetime

# local imports
from db.model import db, Stat, app


@app.route("/api/stats/<country>")
def stats(country):
    """
    grab the total confirmed, deaths, and recovered cases for the country
    """
    # variables
    today = datetime.now().date()

    # search db
    result = Stat.query.filter_by(date=today, country=country).first()

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
    # variables
    today = datetime.now().date()

    # search db
    confirmed, recovered, deaths = (
        db.session.query(
            db.func.sum(Stat.confirmed),
            db.func.sum(Stat.recovered),
            db.func.sum(Stat.deaths),
        )
        .filter_by(date=today)
        .first()
    )

    # return
    return {"confirmed": confirmed, "recovered": recovered, "deaths": deaths}, 200


@app.route("/api/plot/<country>")
def history(country):
    """
    pull all historic data on country
    """
    # use filter to get all data
    result = Stat.query.filter_by(country=country).all()

    # transform result
    array = [
        {
            "confirmd": record.confirmd,
            "date": record.date,
            "recovered": record.recovered,
            "deaths": record.deaths,
        }
        for record in result
    ]
    # return
    return {"result": array}, 200


@app.route("/api/predict/<country>")
def predict(country):
    """
    retreived the prediction for country
    """
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()
