from confluent_kafka import Producer, Consumer
from kafkaglobal import get_kafka_producer, get_kafka_consumer
import json
import time

# this module does nothing but consume from one topic, wait and
# post to another topic in order to illustrate a payment system

if __name__ == "__main__":

    consumer = get_kafka_consumer("one", "latest", "false")
    producer = get_kafka_producer()

    consumer.subscribe(["booking"])
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
            print(type(message))
            time.sleep(4)
            producer.produce("payment", "Payment accepted")
            producer.flush()

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()