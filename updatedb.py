from tinydb import TinyDB, Query
import json

db = TinyDB('db.json')

gappsgroups = db.all()

def getCurrentConfig():
	print('=============================')
	print('Listing current configuration')
	print('=============================')

	for index, group in enumerate(gappsgroups):
		print(index, group['gappslist'] + ' contains: ')
		for member in group['members']:
			print('(' + member['attribute'] + '=' + member['value'] + ')')
		print('=============================')

def main():
	print('1. List All Syncs')
	print('2. Add Group Sync')
	print('3. Delete Group Sync')
	selection = int(raw_input('What would you like to do?'))
	if (selection == 1):
		getCurrentConfig()

if __name__ == '__main__':
    main()