# main.py
import config
from gmail.api import fetch_messages
from scoring.score import decide_label
from gmail.message import GmailMessage
from gmail.label import GmailLabelManager

if __name__ == "__main__":
    # Gmailの元データ取得
    service,full_list = fetch_messages(
        scopes=config.SCOPES,
        limit=config.DEFAULT_FETCH_LIMIT)
    
    # ラベル作成用オブジェクト初期化
    label_manager = GmailLabelManager(service)
    
    gmail_obj = []
    for msg in full_list:
        # 元データからGmailMessageオブジェクト作成
        gmail_obj = GmailMessage(msg)
        # スコア点数取得
        gmail_obj.calc_score()
        # スコアリング判定
        label_name = decide_label(gmail_obj.score)
        # 判定ラベルをGmailに追加
        label_id = label_manager.create_label(label_name)
        # メールをラベリング
        label_manager.add_label(gmail_obj.id,label_id)


