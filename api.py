import requests
import json
from flask_cors import CORS
from flask import request
from confluent_kafka import Producer, Consumer
from kafkaglobal import get_kafka_producer, get_kafka_consumer
from flask import Flask, json
from tinydb import TinyDB, Query
from fetchfunctions import returnBookingFromID, applyChangeToBooking
from seatfunctions import getOrMakeSeatMap, registerSeatBooking

tripsdb = TinyDB("storage/tripsdb.json")
bookingdb = TinyDB("storage/bookingdb.json")

api = Flask(__name__)
CORS(api)

producer = get_kafka_producer()
consumer = get_kafka_consumer("two", "latest", "false")

# for reserving a seat
@api.route("/seatbooking", methods=["POST"])
def registerSeatPOST():
    if (
        ("tripnr" in request.args)
        and ("date" in request.args)
        and ("seat" in request.args)
        and ("bookingID" in request.args)
    ):
        return registerSeatBooking(
            request.args["tripnr"], request.args["date"], request.args["seat"]
        )
    else:
        return "provide seatnumber,  date and tripnr"


# deliver seat map to frontend
@api.route("/getseatmap", methods=["GET"])
def getSeatMap():
    if ("tripnr" in request.args) and ("date" in request.args):
        return getOrMakeSeatMap(request.args["tripnr"], request.args["date"])
    else:
        return "provide date and tripnr to get seat chart"


# return a booking/ticket
@api.route("/getbooking", methods=["GET"])
def getBookings():
    if "bookingID" in request.args:
        requestedBookingID = str(request.args["bookingID"])
        return returnBookingFromID(request.args["bookingID"])
    else:
        return "provide valid ticket number"


# delete booking from db
@api.route("/cancelticket", methods=["POST"])
def cancelTicket():
    Ticket = Query()
    if "bookingID" in request.args:
        requestedBookingID = str(request.args["bookingID"])
        bookingdb.remove(Ticket.bookingID == requestedBookingID)
        return "Cancellation successful"
    else:
        return "provide valid ticket number"


# change time and/or date of booking
@api.route("/changerequest", methods=["POST"])
def changeBookings():
    if (
        ("bookingID" in request.args)
        and ("tripnr" in request.args)
        and ("date" in request.args)
    ):
        bookingID = str(request.args["bookingID"])
        tripnr = str(request.args["tripnr"])
        date = str(request.args["date"])
        return applyChangeToBooking(request.args["bookingID"], tripnr, date)
    else:
        return "provide valid ticket number"


# return trips for given time and destination
@api.route("/trips", methods=["GET"])
def get_trips_from():
    if (
        ("stationcodeFrom" in request.args)
        and ("stationcodeTo" in request.args)
        and ("timefrom" in request.args)
    ):
        stationcodeFrom = str(request.args["stationcodeFrom"])
        stationcodeTo = str(request.args["stationcodeTo"])
        departure = str(request.args["timefrom"])
    else:
        return "provide station codes and departure time in order to get trips"

    Trips = Query()
    results = tripsdb.search(
        (Trips.stationcodeFrom == stationcodeFrom)
        & (Trips.stationcodeTo == stationcodeTo)
        & (Trips.timefrom >= departure)
    )

    print(results)
    return json.dumps(results)


# check payment and register booking to database
@api.route("/bookingrequest", methods=["POST"])
def create_booking_request():
    messagedict = {
        "tripnr": request.args["tripnr"],
        "bookingID": request.args["bookingID"],
        "date": request.args["date"],
    }
    message = json.dumps(messagedict).encode("utf-8")
    producer.produce(
        topic="booking", value=message
    )  # payment service will pick this up
    producer.flush()
    print(message)

    consumer.subscribe(
        ["payment"]
    )  # look for payment apprived/denied, should be a check on booking nr here
    awaitingFeedback = True
    feedback = ""
    try:
        while awaitingFeedback:
            msg = consumer.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print(msg.value().decode("utf8"))
            if msg.value().decode("utf-8") == "Payment accepted":
                bookingdb.insert(messagedict)
                feedback = "Payment accepted"
                awaitingFeedback = False

    except KeyboardInterrupt:
        pass

    return feedback


if __name__ == "__main__":
    api.run()
