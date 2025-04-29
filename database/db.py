import pymssql
import jdatetime
from contextlib import contextmanager
from conf.config import *

@contextmanager
def db_connection():
    conn = pymssql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    try:
        yield conn
    finally:
        conn.close()


def current_jalali_datetime():
    now = jdatetime.datetime.now()
    date_str = now.strftime('%Y/%m/%d')
    time_str = now.strftime('%H:%M')
    return date_str, time_str, f"{date_str}-{time_str}"


class Database:
    def insert_records_to_database(self, temperature):
        date_str, time_str, datetime_str = current_jalali_datetime()

        try:
            with db_connection() as conn, conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO DBTEMP (Date, Time, Temperature, CreateDateTime)
                    VALUES (%s, %s, %s, %s)
                ''', (date_str, time_str, str(temperature), datetime_str))
                conn.commit()
        except Exception as e:
            print(f"[Error] Insert failed: {e}")

    def get_5_temperature(self):
        try:
            with db_connection() as conn, conn.cursor() as cursor:
                cursor.execute('''
                    SELECT TOP 5 Temperature 
                    FROM DBTEMP 
                    ORDER BY id DESC
                ''')
                result = cursor.fetchall()
                return [row[0] for row in result] if result else []
        except Exception as e:
            print(f"[Error] Fetch failed: {e}")
            return []


    def get_last_temperature(self):
        try:
            with db_connection() as conn, conn.cursor() as cursor:
                cursor.execute('''
                    SELECT TOP 1 Temperature, Id 
                    FROM DBTEMP 
                    ORDER BY id DESC
                ''')
                result = cursor.fetchone()
                # print(result)
                return result if result else None
        except Exception as e:
            print(f"[Error] Fetch failed: {e}")
            return None