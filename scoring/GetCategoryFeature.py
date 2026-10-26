# scoring/Get_category_Feature.py
from collections import Counter

"""ラベル別のカテゴリ・重要マーク出現割合を取得"""
def get_category_feature(processed_data):
    features = {}

    for label_name, mails in processed_data.items():

        counter = Counter()

        for mail in mails:
            counter.update(set(mail.get("category", [])))

        total = len(mails)

        features[label_name] = {
            category: count / total
            for category, count in counter.items()
        } if total else {}

    return features