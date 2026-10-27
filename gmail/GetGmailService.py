import os.path
import logging
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
        logging.info("既存トークンファイル読み込み中...")
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
            logging.info("トークンファイルを再取得中...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes
            )
            creds = flow.run_local_server(port=0)

        # トークン保存
        with open(token_file, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    return creds