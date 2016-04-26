from tinydb import TinyDB, Query
import json

db = TinyDB('db.json')

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