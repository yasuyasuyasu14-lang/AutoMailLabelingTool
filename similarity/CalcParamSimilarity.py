import numpy as np
import logging

"""新着メールと各ラベルのパラメータ別類似度を算出"""
def calc_param_similarity(label_features, new_features):
    similarities = {}

    for mail_id, mail_features in new_features.items():

        similarities[mail_id] = {}

        for label_name, label_ft in label_features.items():

            # ① 件名の類似度
            subject_score = _cosine_similarity(
                label_ft["subject"],
                mail_features["subject"]
            )

            # ② 本文の類似度
            body_score = _cosine_similarity(
                label_ft["body"],
                mail_features["body"]
            )

            # ③ 送信者の一致度
            sender_score = sum(
                label_ft["sender"].get(sender, 0.0)
                for sender in mail_features["sender"]
            )

            # ④ カテゴリの一致度
            category_score = (
            sum(
                label_ft["category"].get(category, 0.0)
                for category in mail_features["category"]
            )
            / len(mail_features["category"])
            if mail_features["category"]
            else 0.0
        )

            similarities[mail_id][label_name] = {
                "subject": subject_score,
                "body": body_score,
                "sender": sender_score,
                "category": category_score,
            }

    # 処理件数を表示
    logging.info(f"パラメータ別類似度算出：{len(similarities)}件完了")
    return similarities

def _cosine_similarity(feature_a, feature_b):
    """辞書形式の特徴量からコサイン類似度を算出"""

    common_terms = feature_a.keys() & feature_b.keys()

    dot_product = sum(
        feature_a[term] * feature_b[term]
        for term in common_terms
    )

    norm_a = np.sqrt(
        sum(value ** 2 for value in feature_a.values())
    )

    norm_b = np.sqrt(
        sum(value ** 2 for value in feature_b.values())
    )

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))