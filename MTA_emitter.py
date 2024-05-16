"""
Emitter designed to send a message to a queue on the RabbitMQ server. 
Make sure the RabbitMQ server is on and connected.
Run this and then run the listener.
"""

import pika
import sys
import time
from datetime import datetime
import csv
import logging
import random
import pika.exceptions
from util_logger import setup_logger
# Configure logging
logger, logname = setup_logger(__file__)

input_file_name = "MTAHourlyData50R.csv"

#Defining Functions:
def preprare_message_from_row(row):
    transit_date, transit_time, station_complex_id, station_complex, borough, rideship = row


# CSV Read
def stream_row(input_file_name):
    with open(input_file_name, "r") as input_file:
        reader=csv.reader(input_file, delimiter=",")
        header = next(reader)
        for row in reader:
            yield row
            

def send_message(ns: str = "localhost"):
    """
    Creates and sends a message to the cue with each execution, process runs and finishes.
    """
    try:
        # Creates a blocking connection to the RabbitMQ server
        conection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        ch = conection.channel()

        # Declaring the queue
        ch.queue_declare(queue="MTA_task", durable=True)
        
        for message in stream_row('MTAHourlyData50R.csv'):
            MTAData = ','.join(message)
            # Converting Data to a string
            message = f"{MTAData}"

        # Publish to MTA_task
        ch.basic_publish(
            exchange = "",
            routing_key="MTA_task",
            body=message,
            properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2)
        )
        logging.info(f"[x] Sent '{message}'")
        print(f" [x] sent {message}")
        time.sleep(random.uniform(1, 8)) # random publishing between 1 and 8 seconds
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt. Stopping the program.")
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # Closing the connection
        logging.info("\nclosing connection. Goodby\n")
        conection.close()
if __name__ == "__main__":
    send_message("localhost")




