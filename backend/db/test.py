from model import db, Stat


def main():
    """
    create database and fill it up with stats.. this should only be ran once
    """

    # # init db
    # db.create_all()

    # # create one stat
    # stat = Stat(
    #     id="country2020-01-01", country="Canada", confirmed=1, deaths=1, recovered=1
    # )

    # # commit to db
    # db.session.add(stat)
    # db.session.commit()

    # # check if record is in db
    # print(Stat.query.all())

    # # add another record
    # usa = Stat(id="usa2020-01-01", country="USA", confirmed=1, deaths=0, recovered=0)
    # usa2 = Stat(
    #     id="usa2020-01-02", country="USA", confirmed=1000, deaths=0, recovered=0
    # )
    # db.session.add(usa)
    # db.session.add(usa2)
    # db.session.commit()

    # print(Stat.query.filter_by(country="USA"))

    # # update / upsert
    # q = Stat.query.get({"id": "usa2020-01-03"})
    # print(f"q: {q}")
    # usa3 = Stat(
    #     id="usa2020-01-03", country="USA", confirmed=1000, deaths=0, recovered=0
    # )
    # db.session.add(usa3)
    # db.session.commit()
    # q = Stat.query.filter_by(id="usa2020-01-03")
    # print(f"q2: {q}")

    # q.update({"deaths": 9999})
    # db.session.commit()

    # q = Stat.query.get({"id": "usa2020-01-03"})
    # print(f"q3: {q}")

    # update data
    yemen = Stat.query.get({"id": "Yemen2020-4-19"})
    yemen.confirmed = 9999
    db.session.commit()
    yemen = Stat.query.get({"id": "Yemen2020-4-19"})
    print(yemen)


if __name__ == "__main__":
    main()
