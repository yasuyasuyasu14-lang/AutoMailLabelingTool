# config.py

# 検索サイトURL
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
# Gmail取得件数
DEFAULT_FETCH_LIMIT = 5

# --- スコアリング設定 ---
# ラベルスコア
SCORING_SET = {
    "SENT": 10,
    "STARRED": 10,
    "UNREAD": -3,
    "INBOX": 5,
    "DRAFT": 3,
    "TRASH": -5,
    "SPAM": -10,
    "IMPORTANT": 5,
    "CATEGORY_PERSONAL": 3,
    "CATEGORY_UPDATES": -3,
    "CATEGORY_PROMOTIONS": -3,
    "CATEGORY_SOCIAL": -3,
    "CATEGORY_FORUMS": -3,
}

RECIPIENT_SCORES = {
    "to": 10,
    "cc": -5
}

OTHER_SCORES = {
    "attachment": 10
}

