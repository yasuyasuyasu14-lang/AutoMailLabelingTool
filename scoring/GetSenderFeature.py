from collections import Counter
from email.utils import parseaddr


def get_sender_feature(preprocessed_data, domain_weight=0.5):
    """メールアドレスとドメインの重み付き特徴量を取得"""

    if not 0 <= domain_weight <= 1:
        raise ValueError("domain_weightは0～1で指定してください")

    email_weight = 1.0 - domain_weight

    features = {}

    for label_name, mails in preprocessed_data.items():

        email_counter = Counter()
        domain_counter = Counter()

        # ① 送信者情報を集計
        for mail in mails:

            _, email_address = parseaddr(mail.get("sender", ""))
            email_address = email_address.lower()

            if not email_address or "@" not in email_address:
                continue

            domain = email_address.rsplit("@", 1)[1]

            email_counter[email_address] += 1
            domain_counter[domain] += 1

        total = sum(email_counter.values())

        features[label_name] = {}

        if total == 0:
            continue

        # ② メールアドレスの特徴量
        for email, count in email_counter.items():

            features[label_name][f"email:{email}"] = (
                count / total * email_weight
            )

        # ③ ドメインの特徴量
        for domain, count in domain_counter.items():

            features[label_name][f"domain:{domain}"] = (
                count / total * domain_weight
            )

    return features