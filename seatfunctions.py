from tinydb import TinyDB, Query, where
import json
from confluent_kafka import Producer
from kafkaglobal import get_kafka_producer

mapsdb = TinyDB("storage/seatingmaps.json")
seatbookingsdb = TinyDB("storage/seatbookings.json")
Maps = Query()
Seats = Query()
producer = get_kafka_producer()


def getOrMakeSeatMap(tripnr, date):
    if not mapsdb.contains((Maps.tripnr == tripnr) & (Maps.date == date)):
        mapsdb.insert(
            {
                "date": date,
                "tripnr": tripnr,
                "seats": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0,
                    "10": 0,
                    "11": 0,
                    "12": 0,
                    "13": 0,
                    "14": 0,
                    "15": 0,
                    "16": 0,
                },
            }
        )
        map = mapsdb.get((Maps.tripnr == tripnr) & (Maps.date == date))
        print("map is made" + str(map))
        return map
    else:
        map = mapsdb.get((Maps.tripnr == tripnr) & (Maps.date == date))
        print("map is returned" + str(map))
        return map


def registerSeatBooking(tripnr, date, seat):
    seatbookingsdb.insert({"date": date, "tripnr": tripnr, "seat": seat})
    messagedict = {"date": date, "tripnr": tripnr, "seat": seat}
    message = json.dumps(messagedict).encode("utf-8")
    producer.produce(topic="seats", value=message)
    producer.flush()

    def setSeatReserved(path, value):
        doc = mapsdb.get((Maps.tripnr == tripnr) & (Maps.date == date))

        def transform(doc):
            now = doc
            for key in path[:-1]:
                now = now[key]

            now[path[-1]] = value

        return transform

    strseat = str(seat)
    mapid = mapsdb.get((Maps.tripnr == tripnr) & (Maps.date == date))
    print(mapid)
    mapsdb.update(setSeatReserved(["seats", strseat], 1))
    return "A-ok"
