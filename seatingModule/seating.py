import json
from confluent_kafka import Consumer
from tinydb import TinyDB, Query
from kafkaglobal import get_kafka_consumer

# pretend seating module
# will only keep its own storge updated by consuming booking requests


if __name__ == "__main__":

    consumer = get_kafka_consumer("one", "latest", "false")
    seatbookingsdb = TinyDB("storage/seatbookings.json")
    consumer.subscribe(["seats"])
    try:
        while True:
            msg = consumer.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print(msg.value().decode("utf8"))
            message = json.loads(msg.value().decode("utf8"))
            seatbookingsdb.insert(message)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()
