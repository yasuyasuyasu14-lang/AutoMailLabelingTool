# scoring/Get_category_Feature.py

from collections import Counter


def get_category_feature(preprocessed_data):
    """Gmailカテゴリのラベル別特徴量を取得"""

    features = {}

    for label_name, mails in preprocessed_data.items():

        categories = [
            mail.get("category", "")
            for mail in mails
            if mail.get("category")
        ]

        counter = Counter(categories)

        total = len(categories)

        features[label_name] = {}

        if total == 0:
            continue

        features[label_name] = {
            category: count / total
            for category, count in counter.items()
        }

    return features