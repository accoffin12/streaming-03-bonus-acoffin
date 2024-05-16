"""
Created by: A. C. Coffin
May 2024

Listener Developed for MTA Data using RabbitMQ.
Always Transmit in one terminal and recieve in the other. 
---

This file will output a seperate file MTA_output.txt which cntains all of the transmission data sent from the emitter file.
These will continue unless interupted using CNTL+C, because the emitter contains a loop for all 50 lines from the csv file. 
If you wish to have unique outputs for each code run, change:

output_file_name = "MTA_out.txt" 


"""

import pika
import logging
from util_logger import setup_logger
import sys

# Set up logging:
logger, logname = setup_logger(__file__)

output_file_name = "MTA_out.txt"

# Creating function to generate the Output File:
def callback_func(ch, method, properties, body):
    with open('MTA_output.txt', 'a') as file:
        file.write(body.decode() + '\n') # write message to file


# def process_message(ch, method, properties, body):
    #logger.info(f"Recieved: {body.decode()}")

def process_message(ch, method, properties, body):
    message_time, message_data = body.decode().split(',',1)
    logger.info(f"Recieved: {body.decode()} from {method.routing_key} at {message_time}")
    


# Define the main function to run the program.
# Pass the main and use localhost
def main(hn: str = "localhost"):
    try:
        # Creating block connection to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    except Exception as e:
        logger.error()
        logger.error("ERROR: connection to RabbitMQ server failed.")
        logger.error(f"Verify the server is running on host={connection}.")
        logger.error(f"The error says: {e}")
        logger.error()
        sys.exit(1)
    
    try:
        ch = connection.channel()
        ch.queue_declare(queue="MTA_task", durable=True)
        ch.basic_consume(queue="MTA_task", on_message_callback=callback_func, auto_ack=True)
        #callback_func, queue="MTA_task", on_message_callback=process_message, no_ack=True

        # Print a message to the console:
        logger.info(" [*] Waiting for messages. To exit press CTRL + C")
        ch.start_consuming()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt. Stopping the program.")
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally: 
        logger.info("\nClosing connection. Goodbye \n")
        connection.close()

# If this script is running, exicute functions:
if __name__ == "__main__":
    main()
