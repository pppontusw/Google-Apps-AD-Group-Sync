from tinydb import TinyDB, Query
import json

db = TinyDB('db.json')

def main():
	selection = 0
	while (selection != 'YES') and (selection != 'NO'):
		selection = raw_input('Are you sure you want to purge the database? THIS WILL REMOVE ALL YOUR CONFIGURED SYNCHRONIZATIONS AND FILTERS. Yes / No?').upper()
	if (selection == 'YES'):
		db.purge()
		print('OK!')
		exit(0)
	else:
		exit(0)

if __name__ == '__main__':
    main()