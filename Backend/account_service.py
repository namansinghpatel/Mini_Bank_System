import random
from Database.sqlitedb import sqlitedb

def generate_account_number():
    while True:
        account_number = str( random.randint( 1000000, 9999999 ) )
        if not sqlitedb.account_number_exists(account_number):
            return account_number