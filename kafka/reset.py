
import logging
import psycopg2

from os import environ as ENV
from dotenv import load_dotenv


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


def delete_db(conn) -> None:
    """Clears the interaction, assistance_event and emergency_event tables in the museum database"""

    with open('log_file.txt', 'w'):
        pass

    with conn.cursor() as cur:

        cur.execute("""DELETE FROM rating;""")

        cur.execute("""DELETE FROM call_assistance;""")

        cur.execute("""DELETE FROM call_emergency;""")
        print("--- DELETED ---")

    conn.commit()


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_connection()

    delete_db(conn)
