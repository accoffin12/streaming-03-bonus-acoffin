# streaming-03-bonus-acoffin
Created by A. C. Coffin
Date: 16 May 2024
Northwest Missouri State University
Data Streaming 44671-80/81
Dr. Case

# Overview:
Demonstrating the use of a message broker software, specifically RabbitMQ with MTA Subway Data. 

# Table of Contents:
1. [File List](File_List)
2. [Machine Specs & Terminal Information](Machine_Specs_&_Terminal_Information)
3. [Prerequisites](Prerequisites)
4. [Data Source](Data_Source)
5. [Creating Enviroment & Installs](Creating_an_Enviroment_&_Installs)
6. [Method](Method)
    - [The Emitter/Producer](The_Emitter/Producer)
    - [The Listener/Consumer](The_Listener/Consumer)
7. [Results](Results)


# File List
| File Name | Repo location | Type |
| ----- | ----- | -----|
| util_about.py | utils folder | python script |
| util_aboutenv.py | utils folder | python script |
| util_logger.py | utils folder | python script |
| MTA_emitter.log | logs | log |
| requirements.txt | main repo | text |
| MTAHourlyData50R.csv | main repo | csv |
| MTA_emitter.py | main repo | python script |
| MTA_listener.py | main repo | python script |
| MTA_output.txt | main repo | text |
| EmittingListeningSplit1 | ScreenShots folder | PNG |
| MTA_outputfile1.png | ScreenShots folder | PNG |
| MTA_outputfileMultiLineLoop.png | ScreenShots folder | PNG |


# Machine Specs & Terminal Information
This project was created using a WindowsOS computer with the following Specs. These are not required to run this repository. For further detail on this machine go to the utils folder and open util_output folder to access util_about.txt. The util_about.py was created by NW Missouri State University and added to the repository to provide technical info.

    * Date and Time: 2024-05-16 at 07:50 AM
    * Operating System: nt Windows 10
    * System Architecture: 64bit
    * Number of CPUs: 12
    * Machine Type: AMD64
    * Python Version: 3.11.4
    * Python Build Date and Compiler: main with Jul  5 2023 13:47:18
    * Python Implementation: CPython
    * Terminal Environment:        VS Code
    * Terminal Type:               cmd.exe
    * Preferred command:           python

# Prerequisites
1. Git
2. Python 3.7+ (3.11+ Preferred)
3. VS Code Editor
4. VS Code Extension: Python (by Microsoft)
5. RabbitMQ Server installed and running locally

Be sure that RabbitMQ is installed and turn it on to run. For more information on RabbitMQ and it's installation plese see [RabbitMQ Home Page](https://www.rabbitmq.com/).

# Data Source
Annually millions of people utilize the NYC subways, and constant movement of the population around the city makes it an ideal source to create a fake data stream. The Metropolitan Transportation Authority is responsible for all public transport in New York City and collects data in batches by the hour. This batching creates counts for the number of passengers boarding a subway at a specific station. It also provides data concerning payment, geography, time, date and location of moving populations based on stations. MTA Data is commonly utilized when discussing population movements among districts and the role of public transport.

MTA Data is readily available from New York State from their Portal.

NYC MTA Data for Subways: https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-February-202/wujg-7c2s/about_data

## Modifications of Data
The source contained 12 columns, however the MTAHourlyData50R.csv has 7 columns. In this instance the column originally called "transit_time" has been split, the source had both time and date in the same column. This was addressed by separating time and date into two specific columns, adding a column. The data has also been trimmed from its total of 56.3 million rows to 50 rows. Additionally, time was converted to military time for the sake of loading into the database. 

The columns "payment", "fare", "transfers", "lat", "log" and "geo reference" have been removed as they were not necessary to stream. In this instance our interest is with "transit_date","transit_time", "transit_mode", "station_complex_id", "station_complex,borough" and "ridership". Essentially streaming the number of people who take specific trains, for certain stations in different boroughs during the day. This data is shorter and easier to stream than the original csv. 

# Creating an Enviroment & Installs
RabbitMQ requires the Pika Libarary in order to function, this is addressed through the creation of an enviroment and installing it. Use the following command to create an envrioment, when promted in VS Code set the .env to a workspace folder, select yes.

```
python -m venv .venv # Creates a new enviroment
.\Scripts\activate # activates the enviroment
```

Once the enviroment is created install the following:
```
python -m pip install -r requirements.txt
```
For more information on Pika see the [Pika GitHub](https://github.com/pika/pika)

# Setup Verification
To verify the set up of your enviroment run both util_about.py and util_aboutenv.py found in the util's folder or use the following commands in the terminal.
These commands are structured for WindowsOS if using MacOS or Linux modify to have them function. Also be sure to run pip list in the terminal to check the Pika installation. 
```
python ".\\utils\util_about.py"
python ".\\utils\util_aboutenv.py"
pip list
```
# Method 
In order to stream data utilizing RabbitMQ architecture we need to build both a Producer and Consumer. The Producer publishes the message, which in this case is being pulled from the MTA file that is in the repository. The Consumer decodes and recieves these messages. Both of these are essential to the process and in this case are structured to read from a csv and output a text file that can be stored later. 

## The Emitter/Producer
The Emitter/Producer is a script that allows us to publish data to a queue that can then be recieved by the Consumer. In this particular case there are several steps required to properly stream the MTAHourlyData50R.csv file. These are as follows:
    1. Get the Data
    2. Read the Data
    3. Prepare the data to publish to the queue
    4. Address Complications/Failures
    5. Send the Data

Obtaining the data that would be streamed is a series of steps, the first is establishign the input_file and defining which columns would be used. 

```
input_file_name = "MTAHourlyData50R.csv"

#Defining Functions:
def preprare_message_from_row(row):
    transit_date, transit_time, station_complex_id, station_complex, borough, rideship = row
```
After defining the file to be imported the next challenge was to Read the Data from the file. Rather than writing it to each line individual, using a `yield` indicates that each row generated will be an object instead of a value found when using `return`. 

 These were exicuted first to make the construction of the publishing to the queue simpler. 

```
# CSV Read
def stream_row(input_file_name):
    with open(input_file_name, "r") as input_file:
        reader=csv.reader(input_file, delimiter=",")
        header = next(reader)
        for row in reader:
            yield row
```
In order to create the first iteration of the emitter sans the loop, each step of the following was crafted. All of these blocks have been annotated in the code, and time duration varies between 1 and 8 seconds because of the amount of data being moved between the Producer and Consumer.

```
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
```
Durability was turned on in order to save a copy of th message to the drive, by doing this it makes recieving the message and creating an output file possible. Handling exceptions and interuptsion is important - especially when streaming a large amount of data. This was addressed utilizing the following Exceptions:

```
except KeyboardInterrupt:
        logging.info("KeyboardInterrupt. Stopping the program.")
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
finally:
        # Closing the connection
        logging.info("\nclosing connection. Goodby\n")
        conection.close()
```
The first exception allows for a quick escape using CTRL+C while the second serves as a way to stop the system in case of a failure to connect to RabbitMQ. `finally` dictates that after each of these functions has been exicuted the server conection can be closed after sending the data to the queue named MTA_task.

![Initial Run of Producer and Consumer](/ScreenShots/EmittingListeningSplit1.PNG)

### Adding the Loop
A loop was added so that more than a single line would be sent to the consumer. This means that if the emitter is not interupted that it will emit all 50 lines of the MTAHourlyData50R.csv file. By doing so it demonstrates the possiblity of a Producer continuously emitting different messages to the same queue for the same consumer to recieve so long as the rout_keys and queue names match. 

The addition of the loop did alter the structure of the segment that establishes which task to exicute within the queue or what to do with data sent. 
```
        # Creates a loop to emitt more than one message from the csv
        while True: 
            # Pulls data from the csv file and creates strings that can be read.
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
```
This modification was made after both the MTA_emitter.py and MTA_Listener.py were completed. The resulting stream as well as generated MTA_output.txt are shown. There are several repeat entires near the top, this was due to the experimentation while refactoring the code to ensure that it was sending more than one message. 

![Producer, Consumer and output text](/ScreenShots/MTA_outputfileMultiLineLoop.PNG)

## The Listener/Consumer
The Listener/Consumer serves to recieve data from the queue. In this instance however, the objective is to produce an output text file with the data from the MTAHourlyData50.csv. In order to do this several steps must occur:
    1. Creating an Output File
    2. Function to Process Messages from Queue
    3. Handling Exceptions/FailuresRetrieving the Messages from the queue
    4. Retrieving the Messages from the queue
    5. Exicuting the Script and Getting them

Creating an output file from RabbitMQ requires a few steps. Each of these was completed by the script before the script could be exicuted. 

```
output_file_name = "MTA_out.txt"

# Creating function to generate the Output File:
def callback_func(ch, method, properties, body):
    with open('MTA_output.txt', 'a') as file:
        file.write(body.decode() + '\n') # write message to file

def process_message(ch, method, properties, body):
    message_time, message_data = body.decode().split(',',1)
    logger.info(f"Recieved: {body.decode()} from {method.routing_key} at {message_time}")
```
The `callback_func` was designed specifically to create the file MTA_output.txt, the key was to ensure the file was written with decoded data from the message. If the data is not decoded then the data will be recieved in a csv format. The second fucntion `process_message` was designed to establish what we were pulling from the published message. In this case the most important part is to continue using decode, as this is the second half of interpreting the message sent to the queue.

The next portion was designed to connect the Consumer to the queue. In this case several variation of exception handling, which is a way to handle possible failures. In this case, whether or not 

```
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
```
The second block was designed to address the information within the queue and how we want to strucute it. In this case the code has been modified to accept the loop with an altered variation of `callback_func`. These modfications are crucial if we want the terminal to both write infroamtion to a text file and to accept more than one message being sent in a single stream. 

The original method to recieve only messages and not send them to the output file is commented out but remains as a point of comparison.

```
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
```
Similar to the emitter there are several Exceptions in place to both close the stream with a keyboard interruption or a logging error that the connection failed. Once each of these steps is completed the code may then exicute. The image depicts the initial output prior to the implimentation of the loop. See [Adding the Loop](Adding_the_Loop) for an example of the script recieivng multiple messages that were generated with the loop.

![Run with Consumer and first Ouput](/ScreenShots/MTA_outputfile1.PNG)

# Results:

# Resources:
1. NYC Open Portal: https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-February-202/wujg-7c2s/about_data
2. Pika Information: https://github.com/pika/pika
3. RabbitMQ documentation: https://www.rabbitmq.com/docs
4. RabbitMQ Tutorials: https://www.rabbitmq.com/tutorials
