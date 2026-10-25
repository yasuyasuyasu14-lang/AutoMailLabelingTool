import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def get_gmail_service(scopes):
    creds = _get_credentials(scopes)
    return build('gmail', 'v1', credentials=creds)

def _get_credentials(scopes):
    creds = None
    token_file = 'token.json'

    # トークンファイルがあれば読み込む
    if os.path.exists(token_file):
        print("既存トークンファイル読み込み中...")
        creds = Credentials.from_authorized_user_file(
            token_file, scopes
        )

    # 認証情報がない、または無効な場合
    if not creds or not creds.valid:
        # リフレッシュトークンがあれば更新を試みる
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())

            except:
                # 更新失敗時は再認証する
                creds = None

        # 認証情報がない、または更新に失敗した場合
        if not creds or not creds.valid:
            print("トークンファイルを再取得中...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes
            )
            creds = flow.run_local_server(port=0)

        # トークン保存
        with open(token_file, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    return creds

def _fetch_messages_by_labels(service, label_names, limit):
    result = []
    for label_name in label_names:
        label_id = _get_label_id(service,label_name) # ラベル名からラベルID取得
        if not label_id:
            print(f"ラベル未検出: {label_name}")
            continue

        # 指定ラベルIDでメール情報取得
        messages = service.users().messages().list(
            userId='me',
            labelIds=[label_id],
            maxResults=limit
        ).execute()
        mail_list = messages.get('messages',[])

        for mail in mail_list:
            detail = service.users().messages().get(
                userId='me',
                id=mail['id'],
                format='full'
            ).execute()

            detail["answer_label"] = label_name # ラベル名記録
            result.append(detail)
    return result

