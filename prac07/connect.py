import psycopg2
from config import load_config

def connect():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            print("Connected to the PostgreSQL server.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    connect()