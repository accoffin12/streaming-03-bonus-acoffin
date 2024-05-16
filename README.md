# streaming-03-bonus-acoffin
Created by A. C. Coffin
Date: May 2024
Northwest Missouri State University
Data Streaming 44671-80/81
Dr. Case

# Overview:
Demonstrating the use of a message broker software, specifically RabbitMQ with MTA Subway Data. 

## File List:
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

# Table of Contents:
1. [Machine Specs & Terminal Information](Machine_Specs_&_Terminal_Information:)
2. [Prerequisites](Prerequisites:)
3. [Data Source](Data_Source:)
4. [Creating Enviroment & Installs](Creating_an_Enviroment_&_Installs)


# Machine Specs & Terminal Information:
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

# Prerequisites:
1. Git
2. Python 3.7+ (3.11+ Preferred)
3. VS Code Editor
4. VS Code Extension: Python (by Microsoft)
5. RabbitMQ Server installed and running locally

Be sure that RabbitMQ is installed and turn it on to run. For more information on RabbitMQ and it's installation plese see [RabbitMQ Home Page](https://www.rabbitmq.com/).

# Data Source:
Annually millions of people utilize the NYC subways, and constant movement of the population around the city makes it an ideal source to create a fake data stream. The Metropolitan Transportation Authority is responsible for all public transport in New York City and collects data in batches by the hour. This batching creates counts for the number of passengers boarding a subway at a specific station. It also provides data concerning payment, geography, time, date and location of moving populations based on stations. MTA Data is commonly utilized when discussing population movements among districts and the role of public transport.

MTA Data is readily available from New York State from their Portal.

NYC MTA Data for Subways: https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-February-202/wujg-7c2s/about_data

## Modifications of Data:
The source contained 12 columns, however the MTAHourlyData50R.csv has 13 columns. In this instance the column originally called "transit_time" has been split, the source had both time and date in the same column. This was addressed by separating time and date into two specific columns, adding a 13th column. The data has also been trimmed from its total of 56.3 million rows to 50 rows. Additionally, time was converted to military time for the sake of loading into the database.

# Creating an Enviroment & Installs:
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

# Setup Verification:
To verify the set up of your enviroment run both util_about.py and util_aboutenv.py found in the util's folder or use the following commands in the terminal.
These commands are structured for WindowsOS if using MacOS or Linux modify to have them function. Also be sure to run pip list in the terminal to check the Pika installation. 
```
python ".\\utils\util_about.py"
python ".\\utils\util_aboutenv.py"
pip list
```
