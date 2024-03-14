# Museum Data Processing Pipeline

This Python program is designed to process data from Kafka messages related to a museum's exhibitions and store it in a PostgreSQL database. It listens to a Kafka topic for incoming messages, validates them, and uploads them to the database.

## Features

- **Kafka Integration**: Connects to a Kafka topic to consume incoming messages.
- **Data Validation**: Validates incoming messages to ensure they contain the required fields and have valid values.
- **Database Storage**: Stores validated messages in a PostgreSQL database.
- **Error Logging**: Logs errors encountered during message processing to a log file.

## Requirements

- Python 3.x
- psycopg2 (for PostgreSQL database interaction)
- confluent_kafka (for Kafka integration)
- dotenv (for environment variable management)

## Installation

Install dependencies:

- pip install -r requirements.txt

Setup Environment

- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_IP
- DATABASE_PORT

- BOOTSTRAP_SERVERS
- SECURITY_PROTOCOL
- SASL_MECHANISM
- USERNAME
- PASSWORD

- GROUP
- AUTO_OFFSET


## How To Run

### Run the program using the following command

**python3 consumer.py -l/--log <log_file_path.txt>**

- This will then send all the faulty unusable data to the file path you have selected which should also be a .txt

**python3 consumer.py**

- This will run the program and display everything in the terminal including error messages.

