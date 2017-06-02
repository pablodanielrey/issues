import os
import psycopg2

def getConnection(readonly=False):
    con = psycopg2.connect(
            host=os.environ['ISSUES_DB_HOST'],
            dbname=os.environ['ISSUES_DB_NAME'],
            user=os.environ['ISSUES_DB_USER'],
            password=os.environ['ISSUES_DB_PASSWORD']
        )
    #if readonly:
        #con.autocomit = True
        #con.readonly = True
    return con
