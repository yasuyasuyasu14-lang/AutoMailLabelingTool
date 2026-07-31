import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def fetch_messages(scopes,limit):
    creds = _get_credentials(scopes)
    service = _build_gmail_service(creds)
    messages = _fetch_messages(service, limit)
    return service,messages

def _get_credentials(scopes):
    creds = None
    # トークンファイルがあれば読み込む
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # 無い or 無効なら再認証
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # トークン保存
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def _build_gmail_service(creds):
    return build('gmail', 'v1', credentials=creds)

def _fetch_messages(service, limit):
    base_list = service.users().messages().list(
        userId='me',
        maxResults=limit
    ).execute()
    base_list = base_list.get('messages', [])
    full_list = []
    for msg in base_list:
        full_msg = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()
        full_list.append(full_msg)
    return full_list

"""
messages = results.get('messages', [])

for msg in messages:
    msg_id = msg['id']

    msg_detail = service.users().messages().get(
        userId='me',
        id=msg_id
    ).execute()

    headers = msg_detail['payload']['headers']

    subject = None
    sender = None
    date = None

    for h in headers:
        if h['name'] == 'Subject':
            subject = h['value']
        elif h['name'] == 'From':
            sender = h['value']
        elif h['name'] == 'Date':
            date = h['value']

    print("-----")
    print("Subject:", subject)
    print("From:", sender)
    print("Date:", date)
"""