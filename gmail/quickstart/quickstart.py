import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def delete_emails(service, query):
    try:
        # List all messages matching the query
        response = service.users().messages().list(userId='me', q=query).execute()
        messages = response.get('messages', [])

        # Delete each message
        for message in messages:
            service.users().messages().delete(userId='me', id=message['id']).execute()
            print(f"Deleted message with id: {message['id']}")

        print("All matching emails deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    # Example: Delete all emails in the spam folder
    query = "in:spam"
    delete_emails(service, query)

if __name__ == '__main__':
    main()
