
from collections import Counter
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()

# 集計対象から除外する品詞
EXCLUDE_POS = {
    "助詞",
    "助動詞",
    "記号",
    "接続詞",
}

# 集計対象から除外する文字列
EXCLUDE_WORDS = {
    "ご",
    "お",
}


def calc_features(result, min_thresh_count):
    features = {}

    for label_name, mails in result.items():
        subject_counts = Counter()
        body_counts = Counter()
        sender_counts = Counter()
        category_counts = Counter()

        for mail in mails:
            # 件名の特徴量を集計
            for word in tokenizer.tokenize(mail.get("subject", "")):
                text = word.surface.lower()
                pos = word.part_of_speech.split(",")[0]

                if(pos in EXCLUDE_POS
                    or text in EXCLUDE_WORDS
                    or len(text) <= 1):
                    continue

                subject_counts[text] += 1

            # 本文の特徴量を集計
            for word in tokenizer.tokenize(mail.get("body", "")):
                text = word.surface.lower()
                pos = word.part_of_speech.split(",")[0]

                if pos in EXCLUDE_POS or text in EXCLUDE_WORDS:
                    continue

                body_counts[text] += 1

            # 送信者・カテゴリを集計
            sender = mail.get("sender", "")
            category = mail.get("category", "")

            if sender:
                sender_counts[sender.lower()] += 1

            if category:
                category_counts[category] += 1

        # 出現回数が min_thresh_count 以下の文字列を除外
        features[label_name] = {
            "subject": {
                word: count
                for word, count in subject_counts.items()
                if count > min_thresh_count
            },
            "body": {
                word: count
                for word, count in body_counts.items()
                if count > min_thresh_count
            },
            "sender": dict(sender_counts),
            "category": dict(category_counts),
        }

    return features
