# config.py

# 検索サイトURL
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
# Gmail取得件数
DEFAULT_GET_LIMIT = 50
# ラベル名設定
LABEL_NAMES = {'音楽','就活','重要'}

# 文字列最低出現回数フィルタ
MIN_THRESH_COUNT = 3

# ドメイン重み付け
DOMAIN_WEIGHT = 0.5

# 特徴量の重み付け
FEATURE_WEIGHT = {
    "subject": 0.4,
    "body": 0.2,
    "sender": 0.3,
    "category": 0.1
    }

# ラベル付与の閾値
LABEL_THRESHOLD = 0.3

