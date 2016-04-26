from tinydb import TinyDB, Query
import json

db = TinyDB('db.json')

try:
    import argparse
    flags = argparse.ArgumentParser(description='Initialize the database')
    flags.add_argument('--no-confirm', action='store_true', help='Don\'t prompt for confirmation')
    flags = flags.parse_args()
except ImportError:
    flags = None

def insertIntoDB():
    file = open('initdb.json')
    print (file)
    data = json.load(file)
    print (data)
    db.insert_multiple(data)

def main():
    if (flags.no_confirm):
        selection = 'YES'
    else:
        selection = 0
    while (selection != 'YES') and (selection != 'NO'):
        selection = raw_input('Are you sure you want to re-initialize the database? THIS WILL REMOVE ALL YOUR CONFIGURED SYNCHRONIZATIONS AND REPLACE THEM WITH WHATEVER IS DEFINED IN INITDB.PY. Yes / No?').upper()
    if (selection == 'YES'):
        db.purge()
        insertIntoDB()
        print('OK!')
        exit(0)
    else:
        exit(0)

if __name__ == '__main__':
    main()