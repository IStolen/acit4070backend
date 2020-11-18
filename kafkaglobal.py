from confluent_kafka import Producer, Consumer
import uuid

# insert credentials from report here
uname = ""
pw = ""


def get_kafka_producer():
    return Producer(
        {
            "bootstrap.servers": "pkc-l7q2j.europe-north1.gcp.confluent.cloud:9092",  # needs to be altered for other clusters
            "sasl.mechanism": "PLAIN",
            "security.protocol": "SASL_SSL",
            "sasl.username": uname,
            "sasl.password": pw,
        }
    )


def get_kafka_consumer(groupID, offset, eof):
    return Consumer(
        {
            "bootstrap.servers": "pkc-l7q2j.europe-north1.gcp.confluent.cloud:9092",  # needs to be altered for other clusters
            "sasl.mechanism": "PLAIN",
            "security.protocol": "SASL_SSL",
            "sasl.username": uname,
            "sasl.password": pw,
            "group.id": groupID,
            "auto.offset.reset": offset,
            "enable.partition.eof": eof,
        }
    )
