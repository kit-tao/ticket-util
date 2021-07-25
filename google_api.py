import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pandas as pd


# sample_url: 
# https://docs.google.com/spreadsheets/d/1rXXWQdneb0d4dDQw4LOeLpa8YDTOwvlQl0Ad2xzswXc/edit?usp=sharing

# If modifying these scopes, delete the file token.json.



def get_spreadsheet_data(spreadsheet_id, range_name):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = spreadsheet_id
    SAMPLE_RANGE_NAME = range_name
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credential.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:

        df = pd.DataFrame(values[1:], columns=['Firstname',	'Lastname',	'Email'	,'Ticket',	'Status',	'Date'])
        return df

if __name__ == '__main__':
    

    # The ID and range of a sample spreadsheet.
    # SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    # SAMPLE_RANGE_NAME = 'Class Data!A2:E'

    SAMPLE_SPREADSHEET_ID = '1rXXWQdneb0d4dDQw4LOeLpa8YDTOwvlQl0Ad2xzswXc'
    SAMPLE_RANGE_NAME = 'Sheet1!A2:F'

    data = get_spreadsheet_data(spreadsheet_id=SAMPLE_SPREADSHEET_ID, range_name=SAMPLE_RANGE_NAME)
    print(data)

    
