
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data

import json
import requests

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.google.com/m8/feeds/'
CLIENT_SECRET_FILE = 'client_id (1).json'
APPLICATION_NAME = 'Google Contacts API Python Quickstart'


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
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
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

    credentials = get_credentials()
    contact_client = gdata.contacts.client.ContactsClient()

    auth2token = gdata.gauth.OAuth2TokenFromCredentials(credentials)    

    contacts_client = auth2token.authorize(contact_client)

    new_contact = gdata.contacts.data.ContactEntry()
    # Set the contact's name.
    new_contact.name = gdata.data.Name(
        full_name=gdata.data.FullName(text='Janga Reddy'))
    # Set the contact's phone numbers.
    new_contact.phone_number.append(gdata.data.PhoneNumber(text='dummy number',
        rel=gdata.data.WORK_REL, primary='true'))

    # Send the contact data to the server.
    contact_entry = contact_client.CreateContact(new_contact)
    print "Contact's ID: %s" % contact_entry.id.text
    return contact_entry

if __name__ == '__main__':
    main()
