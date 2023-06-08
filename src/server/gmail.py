import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import time
import base64
from apiclient import errors
from settings import Settings

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class Gmail:

    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(Settings.proj_root,'token.json')):
            creds = Credentials.from_authorized_user_file(os.path.join(Settings.proj_root,'token.json'), SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(Settings.proj_root,'client_secret_560653622901-6ua74dr535io3h7l0e4n60h3o4tb6dra.apps.googleusercontent.com.json'),
                    SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(Settings.proj_root,'token.json'), 'w') as token:
                token.write(creds.to_json())
        if creds != None:
            self.service = build('gmail', 'v1', credentials=creds)
        else:
            raise Exception("Gmail service not initialized")

    def get_email_list(self, email: str):
        results = self.service.users().messages().list(userId='me', q=f'from:{email}').execute()
        return results.get('messages', [])

    def get_email_content_id(self,message_id) -> tuple:

        attach = self.service.users().messages().get(userId='me', id=message_id).execute()
        message_date = int(self.service.users().messages().get(userId='me', id=message_id).execute()['internalDate'])

        header = attach['payload']['headers']
        for values in header:
            if values['name'] == 'Subject':
                subject = values['value']
                if 'Lose It! Daily Summary' not in subject:
                    return None, None
                else:
                    break


        parts = attach.get('payload', [])['parts']

        for i in parts:
            if ('.csv' in i['filename']):
                return i['body']['attachmentId'], message_date

        raise Exception("No CSV found in email")

    def download_msg(self, message_id: str, attachmentid: str):
        attach = self.service.users().messages().attachments().get(userId='me', messageId=message_id, id=attachmentid).execute()
        data = attach['data']
        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        return file_data

    def delete_msg(self, message_id: str):
        self.service.users().messages().delete(userId='me', id=message_id).execute()

    def get_csvs(self, email: str) -> tuple:
        message_list = self.get_email_list(email)
        return_tuple = ([],[])
        for message in message_list:
            message_id = message['id']
            attach_id, message_date = self.get_email_content_id(message_id)
            if attach_id is None:
                continue
            csv_data = self.download_msg(message_id, attach_id)
            return_tuple[0].append(message_date)
            return_tuple[1].append(csv_data)
            #self.delete_msg(message_id)
        return return_tuple


