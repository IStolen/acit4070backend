import json
from tinydb import TinyDB, Query

bookingdb = TinyDB('storage/bookingdb.json')
tripsdb = TinyDB('storage/tripsdb.json')
 

def returnBookingFromID(requestedBookingID):
    Ticket = Query()
    Trip = Query()
    requestedTicket=bookingdb.get(Ticket.bookingID == requestedBookingID)
    requestedTrip = tripsdb.get(Trip.tripID == int(requestedTicket.get('tripnr')))
    result=dict(requestedTrip)
    result2=dict(requestedTicket)
    result.update(result2)
    
    return json.dumps(result)

def applyChangeToBooking(bookingID, tripID, date):
    print(tripID)
    robert = bookingID #for debugging purposes only
    Ticket = Query()
    print(bookingdb.search(Ticket.bookingID == robert))
    bookingdb.update({'tripnr': tripID}, Ticket.bookingID == bookingID)
    print(bookingdb.search(Ticket.bookingID == bookingID))
    return 'change accepted!'   
