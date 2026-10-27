# scoring/Get_New_Feature.py

from email.utils import parseaddr
import logging

def get_new_feature(processed_mails, vectorizer):
    """新着メールごとの特徴量を取得"""

    features = {}

    feature_names = vectorizer.get_feature_names_out()

    for mail in processed_mails:

        mail_id = mail["id"]

        # ① 件名・本文のTF-IDF
        subject_text = " ".join(mail["subject"])
        body_text = " ".join(mail["body"])

        subject_vector = vectorizer.transform([subject_text])
        body_vector = vectorizer.transform([body_text])

        # ② 送信者情報
        _, email_address = parseaddr(mail.get("sender", ""))
        email_address = email_address.lower()

        sender_features = {}

        if email_address and "@" in email_address:

            domain = email_address.rsplit("@", 1)[1]

            sender_features = {
                f"email:{email_address}": 1.0,
                f"domain:{domain}": 1.0,
            }

        # ③ カテゴリ情報
        categories = mail.get("category", [])
        category_features = {
            category: 1.0
            for category in categories
        }

        # ④ 特徴量を格納
        features[mail_id] = {
            "subject": {
                feature_names[index]: float(value)
                for index, value in zip(
                    subject_vector.indices,
                    subject_vector.data
                )
            },
            "body": {
                feature_names[index]: float(value)
                for index, value in zip(
                    body_vector.indices,
                    body_vector.data
                )
            },
            "sender": sender_features,
            "category": category_features,
        }

    # 処理件数を表示
    logging.info(f"新着メール特徴量取得：{len(features)}件完了")
    return features