<p align="center">
  </a>
</p>
<h1 align="center">
  ACIT 4070 exam project - prototype ticketing system backend
</h1>

This project contains an API (Flask) that recieve http-requests and act on them by returning content from the storage (tinydb). It also connects to other services by producing and consuming from a message broker (confluent Kafka).

You'll find the frontend app at https://github.com/IStolen/nrtickets

## 🚀 Start it up

**make sure you have the right python 🐍**

    You need to have python3 and pip installed. 

**make yourself a virtual enviroment**

    Navigate into the directory where you have the project

    $python3 -m venv acit
    $source acit/bin/activate
    $pip install -r requirements.txt

**start up the services**
    Insert credentials into the kafkaglobal-file on each of the services you want to start. 
    If you have your own confluent-cluster, you must also update bootratrap server. 

**start up the services**
    The project has three services. First: the ticket management app that serves data and logic to the gatsby-project with the front end. Secondly, a simple python-script made to imitate a payment service that approves the payment and returns the result to the ticketing app. This script does nothing other than to consume messages fom a Kafka-topic, wait for some seconds and then produce messages to a different Kafka-topic. Third: a seating service similar to the payment service. 
    to start the API (necessary for the front end app to work)

    $python3 api.py

  The API now is active at `http://localhost:5000`
    
  To start the pretend payment service, open a new terminal window where you enter

    $python3 paymentModule/pretendVipps.py

  To start the pretend seating service, open a new terminal window where you enter

    $python3 seatingModule/seating.py
