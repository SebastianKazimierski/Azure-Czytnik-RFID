import pyodbc
import azure.functions as func
import logging
import os


def main(req: func.HttpRequest) -> func.HttpResponse:

    Nr_karty = req.get_json()
    wartosc = Nr_karty["Nr_karty"]
    Nr_kartystring = wartosc
    logging.info(type(Nr_kartystring))
    CARDConString = os.getenv('CARDConString')
    logging.info(f'conString {CARDConString}')

    with pyodbc.connect(CARDConString) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Nr_karty from CARD")
            row = cursor.fetchone()
            flag = 0
            while row:
                logging.info(row[0])
                if Nr_kartystring == row[0]:
                    flag = 1
                row = cursor.fetchone()

    if flag == 0:
        return func.HttpResponse("Odmowa dostepu", status_code=401)
    if flag == 1:
        return func.HttpResponse('Dostep uzyskany', status_code=202)
