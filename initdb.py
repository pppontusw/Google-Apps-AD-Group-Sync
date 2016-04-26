from tinydb import TinyDB, Query
import json

db = TinyDB('db.json')

def insertIntoDB():
    db.insert_multiple([{
        'gappslist': 'nordics@example.com',
        'members': [
            {
            'attribute': 'physicalDeliveryOfficeName',
            'value': 'Denmark'
            },
            {
            'attribute': 'physicalDeliveryOfficeName',
            'value': 'Sweden'
            },
            {
            'attribute': 'physicalDeliveryOfficeName',
            'value': 'Norway'
            },
            {
            'attribute': 'physicalDeliveryOfficeName',
            'value': 'Finland'
            },
        ],
        'type': 'OR'
        },
        {
        'gappslist': 'IT-US@example.com',
        'members': [
            {
            'attribute': 'physicalDeliveryOfficeName',
            'value': 'USA'
            },
            {
            'attribute': 'Department',
            'value': 'IT'
            },
        ],
        'type': 'AND'
    }])

def main():
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