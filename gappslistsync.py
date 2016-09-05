import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from ConfigParser import SafeConfigParser

import ldap
from tinydb import TinyDB, Query
import json

import logging
import sys
import datetime

logging.getLogger("oauth2client").setLevel(logging.WARNING)
logger = logging.getLogger('gappslistsync')
logger.setLevel(logging.INFO)
file = logging.FileHandler('gappslistsync.log')
file.setLevel(logging.INFO)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file.setFormatter(logging.Formatter('%(message)s'))
console.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(file)
logger.addHandler(console)

db = TinyDB('db.json')

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser], description='Synchronize Google Groups with Active Directory lists or attributes')
    flags.add_argument('--service-account', action='store_true', help='Use service account credentials')
    flags.add_argument('--simulate', action='store_true', help='Don\'t make changes to Google Apps')
    flags.add_argument('--do-remove', action='store_true', help='REMOVE users who does not match the criteria from the Google Apps Group')
    flags = flags.parse_args()
except ImportError:
    flags = None

try:
    parser = SafeConfigParser()
    parser.read('config.ini')
except:
    exit()

#API Scope and Application name to use when asking for user permission
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user', 'https://www.googleapis.com/auth/admin.directory.group']
APPLICATION_NAME = 'Google Apps AD Group Sync'

if (flags.service_account):
    try:
        #Path to the Service Account's Private Key file
        SERVICE_ACCOUNT_JSON_FILE_PATH = parser.get('Google_Config', 'SERVICE_ACCOUNT_JSON_FILE_PATH')
        #User that Service Account will impersonate (must be the email of a primary domain superadmin)
        SERVICE_ACCOUNT_IMPERSONATE_ACCOUNT = parser.get('Google_Config', 'SERVICE_ACCOUNT_IMPERSONATE_ACCOUNT')
    except Exception as e:
        logger.warning(e)
else:
    try:
        #Client ID file of service account
        CLIENT_SECRET_FILE = parser.get('Google_Config', 'CLIENT_SECRET_FILE_PATH')
    except Exception as e:
        logger.warning(e)

try:
    #LDAP settings
    LDAPUrl = parser.get('AD_Config', 'LDAPUrl')
    LDAPUserDN = parser.get('AD_Config', 'LDAPUserDN')
    LDAPUserPassword = parser.get('AD_Config', 'LDAPUserPassword')
    LDAPBaseDN = parser.get('AD_Config', 'LDAPBaseDN')
    try: 
        LDAPAllUserGroupDN = parser.get('AD_Config', 'LDAPAllUserGroupDN')
    except:
        logger.warning(e)
except Exception as e:
    logger.warning(e)

def get_sacredentials():

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_JSON_FILE_PATH, SCOPES)

    delegated_credentials = credentials.create_delegated(SERVICE_ACCOUNT_IMPERSONATE_ACCOUNT)
    
    return delegated_credentials

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'admin-directory_v1-gapps-ad-group-sync.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
    return credentials

def getGroupMembersGAPI(service, group):

    results = service.members().list(groupKey=group).execute()

    groups = results.get('members', [])

    memberlist = []

    for group in groups:
        memberlist.append(group['email'])

    return memberlist

def addMemberToGroupGAPI(service, group, member):

    memberjson = {
        'email': member
    }

    try:
        results = service.members().insert(groupKey=group, body=memberjson).execute()
    except Exception as e:
        logger.warning(e)
        

def removeMemberFromGroupGAPI(service, group, member):

    results = service.members().delete(groupKey=group, memberKey=member).execute()


def main():
    logger.info('RUN STARTED AT %s' % datetime.datetime.now())
    # Check if we are using a service account to connect or launch the browser for interactive logon
    if (flags.service_account):
        credentials = get_sacredentials()
    else:
        credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    # Connect to the LDAP server
    ldapconn = ldap.initialize(LDAPUrl)
    ldapconn.set_option(ldap.OPT_REFERRALS,0)

    # Bind to LDAP server
    try:
        ldapconn.simple_bind_s(LDAPUserDN, LDAPUserPassword)
    except ldap.INVALID_CREDENTIALS:
        logger.error("LDAP ERROR: Your username or password is incorrect")
    except ldap.LDAPError, e:
        logger.error(e)

    # Create LDAP filter
    if LDAPAllUserGroupDN:
        baseldapfilter = '(&' + '(objectclass=person)(memberof=' + LDAPAllUserGroupDN + ')'
    else:
        baseldapfilter = '(&' + '(objectclass=person)'

    # Read group configuration from DB
    gappsgroups = db.all()

    # Load each group that we are processing
    for group in gappsgroups:
        # Get all the members of this group
        gappsmembers = getGroupMembersGAPI(service, group['gappslist'])
        # And convert to lowercase
        gappsmembers = [gmember.lower() for gmember in gappsmembers]
        # Create the base filter
        ldapfilter = list()
        ldapfilter.append(baseldapfilter)
        # Step through the member values
        for operation in group['members']:
            # Construct the search filter
            if (operation['attribute'] == "LDAPQuery"):
                ldapfilter.append(operation['value'])
            else:
                if (type(operation['value']) == list):
                    # If array = OR
                    construction = '(|'
                    for value in operation['value']:
                        construction += '(' + operation['attribute'] + '=' + value + ')'
                    construction += ')'
                    ldapfilter.append(construction)
                else:
                    # AND
                    ldapfilter.append('(' + operation['attribute'] + '=' + operation['value'] + ')')
        ldapfilter.append(')')
        searchfilter = ''.join(ldapfilter)
        # Search for all users who match the criteria to be in this group
        ldapsearch = ldapconn.search_s(LDAPBaseDN, ldap.SCOPE_SUBTREE, searchfilter, ['samAccountName','mail','memberOf'])
        # If users should be removed we need to collect a list of all emails in our LDAP search so we can remove those who don't appear here
        if (flags.do_remove):
            usermailarray = []
        # Step through users that should be in this group
        for user in ldapsearch:
            attr = user[1]
            mail = attr['mail']
            # Splice (can only have one primary email anyway) and lowercase
            mail = mail[0].lower()
            # If we have --do-remove we want to ensure we save them here so we do not remove any valid members
            if (flags.do_remove):
                usermailarray.append(mail)
            # Filter out the users who already exists in the group
            if (mail not in gappsmembers):
                if (flags.simulate):
                    logger.info(mail + ' would be added to: ' + group['gappslist'])
                else:
                    # And finally add the ones who don't
                    addMemberToGroupGAPI(service, group['gappslist'], mail)
                    logger.info(mail + ' was added to: ' + group['gappslist'])
        if (flags.do_remove):
            for member in gappsmembers:
                # Lowercase again!
                member = member.lower()
                # Filter out the members who aren't supposed to be in this group
                if (member not in usermailarray):
                    if (flags.simulate):
                        logger.info(member + ' would be removed from: ' + group['gappslist'])
                    else:
                        # Delete each user that are not supposed to be here
                        removeMemberFromGroupGAPI(service, group['gappslist'], member)
                        logger.info(member + ' was removed from: ' + group['gappslist'])

    
    ldapconn.unbind()

if __name__ == '__main__':
    main()
