from __future__ import print_function

import datetime
import os.path

from dotenv import load_dotenv
import os


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.models.Event import Event

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']



load_dotenv('.env2')

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
print(client_id, client_secret)

if (client_id or client_secret) is None:
    raise ValueError('Env is not correctly setted')
    

# Load client configuration from JSON file
client_config = {
	"installed": {
		"client_id": client_id,
		"client_secret": client_secret,
		"project_id": "ihzonaid",
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://oauth2.googleapis.com/token",
		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		"redirect_uris": ["http://localhost"]
	}
}


token_location = "resource/token.json"

def calender_api(event):
    creds = None
    if os.path.exists(token_location):
        creds = Credentials.from_authorized_user_file(token_location, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_location, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        cratedEvent = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (cratedEvent.get('htmlLink')))
        return cratedEvent.get('status')

    except HttpError as error:
        if error.status_code == 400:
            print("Bad request")
        print('An error occurred: %s' % error)
