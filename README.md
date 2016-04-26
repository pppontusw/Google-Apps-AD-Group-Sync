# Google Apps & Active Directory dynamic groups sync

## What does it do?

Updates your Google Apps Groups members based on attributes and filters stored in an LDAP server such as Microsoft Active Directory. This can be used to make dynamic groups, for example you can make a group that include everyone with 'Sweden' in the Office-field in AD and will update whenever a new account is created and this field is added.

## Prerequisites

python-dev
libldap2-dev
libsasl2-dev
libssl-dev

```sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev``` on Debian/Ubuntu

```
pip install --upgrade google-api-python-client
pip install python-ldap
pip install tinydb
```

## Required configuration

You will need to fill in the config.ini:

```
[AD_Config]
LDAPBaseDN=OU=OrgUnit,DC=example,DC=com
LDAPUrl=ldap://example.com
LDAPUserDN=gadgs@example
LDAPUserPassword=notapassword
#A common group for all users - any users not in this group will not be processed
LDAPAllUserGroupDN=CN=GoogleUsers,OU=OrgUnit,DC=example,DC=com

[Google_Config]
CLIENT_SECRET_FILE_PATH = client_secret.json
# Path to the secret_key if you use a domain wide service account - otherwise this is not needed
SERVICE_ACCOUNT_JSON_FILE_PATH = secret_key.json
#Needs to be an account with superadmin permission - only needed if you use a domain wide service account
SERVICE_ACCOUNT_IMPERSONATE_ACCOUNT = superadmin@example.com
```

Then you have to populate the database (db.json), you can do this one of two ways: 

**If you are comfortable with JSON**

Use the initdb.py script and modify the db.insert_multiple() function to insert all your lists. You can also use listdb.py to list your configuration and purgedb.py to empty the database.

```
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
```

**If you are not comfortable with JSON**

Use the updatedb.py script to interactively add your lists and filters to the database.



And then finally configure an account to use according to below instructions:

## To use a service account through one time logon

1. Use https://console.developers.google.com/start/api?id=admin to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.

2. At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.

3. Select the Credentials tab, click the Add credentials button and select OAuth 2.0 client ID.

4. Select the application type Other, enter the name "Google Apps AD List Sync, and click the Create button.

5. Click OK to dismiss the resulting dialog.

6. Click the file_download (Download JSON) button to the right of the client ID.

7. Move this file to your working directory and rename it client_secret.json.



## To use a domain wide service account: 

1. Set up a service account at https://console.developers.google.com/start/api?id=admin

2. Authorize for Directory API Quickstart

3. Download the json secret, note the Client ID and email address. The JSON secret key should be places in the root folder and called secret_key.json.

4. Go to your Google Apps domain’s Admin console.

5. Select Security from the list of controls. If you don't see Security listed, select More controls from the gray bar at the bottom of the page, then select Security from the list of controls.

6. Select Advanced settings from the list of options.

7. Select Manage API client access in the Authentication section.

8. In the Client name field enter the service account's Client ID.

9. In the One or More API Scopes field enter the list of scopes that your application should be granted access to. For example if you need domain-wide access to Users and Groups enter: https://www.googleapis.com/auth/admin.directory.user, https://www.googleapis.com/auth/admin.directory.group

10. Click the Authorize button.