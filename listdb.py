from tinydb import TinyDB, Query
import json

db = TinyDB('db.json')

def getCurrentConfig():
	print('=============================')
	print('Listing current configuration')
	print('=============================')

	gappsgroups = db.all()

	for index, group in enumerate(gappsgroups):
		print (group['gappslist'])
		print('ID: ' + str(group.eid)) 
		for member in group['members']:
			print('(' + member['attribute'] + '=' + member['value'] + ') ' + group['type'])
		print('=============================')

def main():
	getCurrentConfig()
	exit(0)

if __name__ == '__main__':
    main()