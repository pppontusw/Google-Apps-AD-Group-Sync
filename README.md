# Google Apps & Active Directory dynamic groups sync

1. Install prerequisites

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

## To use a service account through one time logon


Use https://console.developers.google.com/start/api?id=admin to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
Select the Credentials tab, click the Add credentials button and select OAuth 2.0 client ID.
Select the application type Other, enter the name "Google Apps AD List Sync, and click the Create button.
Click OK to dismiss the resulting dialog.
Click the file_download (Download JSON) button to the right of the client ID.
Move this file to your working directory and rename it client_secret.json.



## To use a domain wide service account: 

Set up a service account at https://console.developers.google.com/start/api?id=admin

Authorize for Directory API Quickstart

Download the json secret, note the Client ID and email address. The JSON secret key should be places in the root folder and called secret_key.json

```Go to your Google Apps domain’s Admin console.
Select Security from the list of controls. If you don't see Security listed, select More controls from the gray bar at the bottom of the page, then select Security from the list of controls.
Select Advanced settings from the list of options.
Select Manage API client access in the Authentication section.
In the Client name field enter the service account's Client ID.
In the One or More API Scopes field enter the list of scopes that your application should be granted access to (see image below). For example if you need domain-wide access to Users and Groups enter: https://www.googleapis.com/auth/admin.directory.user, https://www.googleapis.com/auth/admin.directory.group
Click the Authorize button.```

You will need to fill in an email address of a super administrator that your service account will impersonate