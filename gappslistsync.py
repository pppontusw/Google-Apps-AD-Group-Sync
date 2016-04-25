from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from ConfigParser import SafeConfigParser

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser], description='Synchronize Google Groups with Active Directory lists or attributes')
    flags.add_argument('--service-account', action='store_true', help='Use service account credentials')
    flags = flags.parse_args()
except ImportError:
    flags = None

try:
    parser = SafeConfigParser()
    parser.read('config.ini')
except:
    print('config.ini is either invalid or does not exist. Please verify your config.ini file.')

#API Scope and Application name to use when asking for user permission
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
APPLICATION_NAME = 'Google Apps AD Group Sync'

#Client ID file of service account
CLIENT_SECRET_FILE = parser.get('Google_Config', 'CLIENT_SECRET_FILE')
#Email of the Service Account
SERVICE_ACCOUNT_EMAIL = parser.get('Google_Config', 'SERVICE_ACCOUNT_EMAIL')
#Path to the Service Account's Private Key file
SERVICE_ACCOUNT_JSON_FILE_PATH = parser.get('Google_Config', 'SERVICE_ACCOUNT_JSON_FILE_PATH')
#User that Service Account will impersonate (must be the email of a primary domain superadmin)
SERVICE_ACCOUNT_IMPERSONATE_ACCOUNT = parser.get('Google_Config', 'SERVICE_ACCOUNT_IMPERSONATE_ACCOUNT')


def get_sacredentials():

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_JSON_FILE_PATH, SCOPES)

    delegated_credentials = credentials.create_delegated(SERVICE_ACCOUNT_IMPERSONATE_ACCOUNT )
    
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
        print('Storing credentials to ' + credential_path)
    return credentials

def main():

    # Check if we are using a service account to connect or launch the browser for interactive logon
    if (flags.service_account):
        credentials = get_sacredentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('admin', 'directory_v1', http=http)
    else:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('admin', 'directory_v1', http=http)

    print('Getting the first 10 users in the domain')

    #results = http.request('https://www.googleapis.com/admin/directory/v1/users?domain=universumglobal.com&maxResults=10&orderBy=email')

    results = service.users().list(customer='my_customer', maxResults=10,
        orderBy='email').execute()

    #print(results)
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print('{0} ({1})'.format(user['primaryEmail'],
                user['name']['fullName']))


if __name__ == '__main__':
    main()