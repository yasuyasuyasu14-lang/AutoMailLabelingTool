# scoring/Get_category_Feature.py
from collections import Counter
import logging

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

    # 処理件数を表示
    count = sum(len(mails) for mails in processed_data.values())
    logging.info(f"カテゴリ特徴量取得：{count}件完了")
    return features