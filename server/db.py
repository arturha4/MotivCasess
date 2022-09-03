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


@try_connection
def create_psql_view(cursor):
    cursor.execute(
        """CREATE VIEW domains AS 
        SELECT url, usd_course
        FROM web_sites
        """
    )

def get_web_site_by_hash(hash):
    conn=get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
        SELECT * FROM web_sites WHERE hash='{0}';
        """.format(hash))
        data=cursor.fetchall()[0]
    if conn:
        cursor.close()
        conn.close()
    return {
        'id': data[0],
        'hash': data[1],
        'includeTime': data[2],
        'usd_course': data[3],
        'url': data[4]
    }

def create_web_sites(func):
    connection = get_connection()
    with connection.cursor() as cursor:
        dataText = ','.join(cursor.mogrify('(%s,%s,%s,%s)', row).decode("utf-8") for row in func())
        sqlText = """INSERT INTO web_sites (hash,includeTime, usd_course, url) values {0}""".format(dataText)
        cursor.execute(sqlText)
    if connection:
        cursor.close()
        connection.close()

print(int('1BB8B7F8A6F86C992D8F8982244C5A42',16))