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

def addSync():
	print('=============================')
	print('Add Group Sync')
	print('=============================')
	newgroupname = raw_input('What is the primary email address of the group in Google Apps?')
	print (newgroupname)
	newgrouptype = 'OR'
	attribute = raw_input('What attribute would you like to filter on?')
	value = raw_input('What value should this attribute contain?')
	members = [{ 'attribute': attribute, 'value': value }]
	continueadd = 0
	while (continueadd != 'NO') and (continueadd != 'YES'):
		continueadd = raw_input('Would you like to add another attribute/value filter? Yes / no?').upper()
	if (continueadd == 'YES'):
		newgrouptype = 0
		print('Would you like this group to contain all members matching any criteria you define (OR) or only those matching all criteria (AND)')
		while (newgrouptype != 'AND') and (newgrouptype != 'OR'):
			newgrouptype = raw_input('OR / AND?')
			newgrouptype = newgrouptype.upper()
		while (continueadd != 'NO'):
			attribute = raw_input('What attribute would you like to filter on?')
			value = raw_input('What value should this attribute contain?')
			members = members + [{ 'attribute': attribute, 'value': value }]
			continueadd = raw_input('Would you like to add another attribute/value filter? Yes / no?').upper()
	
	groupsync = { 'gappslist': newgroupname, 'type': newgrouptype, 'members': members }
	print('=============================')
	print('Will add group ' + newgroupname + ' with members')
	for member in members:
		print('(' + member['attribute'] + '=' + member['value'] + ') ' + newgrouptype)
	print('=============================')
	correct = 0
	while (correct != 'YES') and (correct != 'NO'):
		correct = raw_input('Is this correct? Yes / no?').upper()
	if (correct == 'YES'):
		db.insert(groupsync)
		print('OK!')
		print('=============================')
		main()
	else:
		print('Not added')
		print('=============================')
		main()

def removeSync():
	gappsgroups = db.all()
	gappsgroupids = []
	for group in gappsgroups:
		gappsgroupids.append(group.eid)
	print gappsgroupids
	quitting = 0
	while (quitting != 'YES'):
		toremove = 0
		while (toremove not in gappsgroupids):
			getCurrentConfig()
			toremove = int(raw_input('Enter the ID of the list to remove?'))
		sure = 0
		while (sure != 'YES') and (sure != 'NO'):
			zeroindex = toremove-1
			print('THIS WILL DELETE THE CONFIGURATION FOR ' + gappsgroups[zeroindex]['gappslist'])
			sure = raw_input('Are you sure? Yes / No?').upper()
		if (sure == 'YES'):
			print(toremove)
			db.remove(eids=[toremove])
			print('OK!')
			while (quitting != 'NO') and (quitting != 'YES'):
				quitting = raw_input('Would you like to exit and go back to the main menu? Yes / No?').upper()
		else:
			print('Not deleted')
			while (quitting != 'NO') and (quitting != 'YES'):
				quitting = raw_input('Would you like to exit and go back to the main menu? Yes / No?').upper()


def main():
	selection = 0
	while (selection != 4):
		print('Menu')
		print('=============================')
		print('1. List All Syncs')
		print('2. Add Group Sync')
		print('3. Delete Group Sync')
		print('4. Exit')
		selection = int(raw_input('What would you like to do?'))
		if (selection == 1):
			getCurrentConfig()
		elif (selection == 2):
			addSync()
		elif (selection == 3):
			removeSync()

	exit(0)

if __name__ == '__main__':
    main()