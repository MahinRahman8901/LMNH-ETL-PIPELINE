"""Pipeline that cleans data from a data stream from LMNH
and uploads it to a database
"""

import datetime
import json
import logging
import time
import psycopg2

from os import environ as ENV
from argparse import ArgumentParser
from dotenv import load_dotenv
from confluent_kafka import Consumer

SITES = ['0', '1', '2', '3', '4', '5', ]
VAL = [-1, 1, 2, 3, 4]
TYPE = [0, 1]
CALL_ASSISTANCE = 0
CALL_EMERGENCY = 1


def setup_logging(log_file):
    """
    Set up logging configuration.
    """
    logging.basicConfig(filename=log_file,
                        level=logging.ERROR, format='%(message)s')


def get_db_connection():
    """
    Establishes a connection to the database.
    Returns:
        Database connection object.
    """
    load_dotenv()
    try:
        return psycopg2.connect(
            dbname=ENV["DATABASE_NAME"],
            user=ENV["DATABASE_USER"],
            password=ENV["DATABASE_PASSWORD"],
            host=ENV["DATABASE_IP"],
            port=ENV["DATABASE_PORT"]
        )
    except Exception as e:
        print("Error: Cannot connect to the database")
        logging.error(f'Error connecting to the database: {e}')


def consumer() -> Consumer:
    """
    Initializes a Kafka consumer.
    Returns:
       Kafka Consumer Object.
    """
    c = ({
        'bootstrap.servers': ENV["BOOTSTRAP_SERVERS"],
        'security.protocol': ENV["SECURITY_PROTOCOL"],
        'sasl.mechanisms': ENV["SASL_MECHANISM"],
        'sasl.username': ENV["USERNAME"],
        'sasl.password': ENV["PASSWORD"],
        'group.id': ENV['GROUP'],
        'auto.offset.reset': ENV['AUTO_OFFSET']
    })
    return Consumer(c)


def handle_message(message) -> str:
    """
    Handles the incoming Kafka message.
    Returns:
        dict or str: Processed message or error message.
    """
    if "at" not in message:
        return "Error: Missing 'at' Key"

    date_str = message.get('at')
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError as e:
        logging.error(f"Invalid date format: {e}")
        return f"Error: Invalid date format - {e}"

    hour = date.hour
    minute = date.minute
    if hour < 8 or (hour == 8 and minute < 45):
        return "Error: Invalid Museum Not Open"
    if hour > 18 or (hour == 18 and minute > 15):
        return "Error: Invalid Museum is Closed"

    if "site" not in message:
        return "Error: Invalid Missing 'site' Key"
    if message.get("site") not in SITES:
        return "Error: Invalid site Value Must Be Between 0-5"
    if "val" not in message:
        return "Error: Invalid Missing 'val' Key"
    if message.get("val") not in VAL:
        return "Error: Invalid val Value Must Be Between -1 -> 4 (Excl 0)"

    if "type" in message:
        if message.get("type") not in TYPE:
            return "Error: Invalid type has to be either 0 or 1"

    return message


def send_valid_message_to_db(conn, location):
    """
    Inserts a valid message into the database.
    """
    at = location["at"]
    site = int(location["site"]) + 1
    val = int(location["val"]) + 1

    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO rating (rating_timestamp, rating_value, exhibition_id)
                        VALUES (%s, %s, %s)
                    """, (at, val, site))
    conn.commit()
    logging.info('---Database Upload Complete---')


def send_valid_emergency(conn, location):
    """
    Inserts a valid emergency message into the database.
    """
    at = location["at"]
    site = int(location["site"]) + 1

    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO call_emergency (call_emergency_timestamp, exhibition_id)
                        VALUES (%s, %s)
                    """, (at, site))
    conn.commit()
    logging.info('---Emergency Upload Complete---')


def send_valid_assistance(conn, location):
    """
    Inserts a valid assistance message into the database.
    """
    at = location["at"]
    site = int(location["site"]) + 1

    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO call_assistance (call_assistance_timestamp, exhibition_id)
                        VALUES (%s, %s)
                    """, (at, site))
    conn.commit()
    logging.info('---Assistance Upload Complete---')


def upload_to_database(conn, location):
    """
    Uploads the processed message to the database.
    """
    if location["val"] == -1 and location["type"] == CALL_ASSISTANCE:
        send_valid_assistance(conn, location)
    if location["val"] == -1 and location["type"] == CALL_EMERGENCY:
        send_valid_emergency(conn, location)

    send_valid_message_to_db(conn, location)


def load_message(c: Consumer, conn, log_file=None):
    """
    Loads messages from Kafka and processes them.
    """
    c.subscribe(["lmnh"])
    setup_logging(log_file) if log_file else None

    try:
        while True:
            message = c.poll(1.0)
            if message is None:
                time.sleep(1)
                continue
            if message.error():
                logging.error(f"Kafka error: {message.error()}")
            else:
                value = json.loads(message.value().decode())
                check_message = handle_message(value)

                if "Error" in check_message:
                    if log_file:
                        logging.error(check_message)
                    else:
                        print(check_message)
                else:
                    print("Valid Message:", check_message)
                    upload_to_database(conn, check_message)

                    time.sleep(2)

    except KeyboardInterrupt:
        print("Incorrect Input")
    finally:
        c.close()


if __name__ == "__main__":

    parser = ArgumentParser(description='ETL Script with Logging')
    parser.add_argument('-l', '--log', dest='log_file',
                        help='Enable logging and specify the log file path')

    args = parser.parse_args()

    load_dotenv()

    conn = get_db_connection()

    c = consumer()
    load_message(c, conn, log_file=args.log_file)
