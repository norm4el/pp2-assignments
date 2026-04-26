

import psycopg2
from config import load_config


def get_connection():
    conf = load_config()
    return psycopg2.connect(**conf)