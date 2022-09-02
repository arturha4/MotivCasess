import psycopg2
import psycopg2.extras
from cfg import *


def get_connection():
    connection = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    connection.autocommit = True
    return connection


def try_connection(func):
    def wrapper(*args):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                if args:
                    func(cursor, *args)
                else:
                    func(cursor)
        except Exception as ex:
            print("Error", ex)
        finally:
            if connection:
                connection.close()
                print("Connection closed")

    return wrapper


@try_connection
def delete_table(cursor):
    cursor.execute(
        """DROP TABLE web_sites;"""
    )


@try_connection
def create_table(cursor):
    cursor.execute(
        """CREATE TABLE web_sites(
        id SERIAL PRIMARY KEY,
        hash text NOT NULL,
        includeTime timestamp NOT NULL,
        usd_course numeric NOT NULL,
        url text NOT NULL );"""
    )


def create_web_sites_fast(func):
    connection = get_connection()
    with connection.cursor() as cursor:
        dataText = ','.join(cursor.mogrify('(%s,%s,%s,%s)', row).decode("utf-8") for row in func())
        sqlText = """INSERT INTO web_sites (hash,includeTime, usd_course, url) values {0}""".format(dataText)
        cursor.execute(sqlText)
    if connection:
        cursor.close()
        connection.close()

