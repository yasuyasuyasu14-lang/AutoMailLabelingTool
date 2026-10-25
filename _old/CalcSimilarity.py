from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calc_similarity(label_data, new_mail):
    # 各メールの情報を1つの文字列にまとめる
    def make_text(mail):
        return " ".join([
            mail.get("subject", ""),
            mail.get("body", ""),
            mail.get("sender", ""),
            mail.get("category", ""),
        ])

    # 各ラベルのメールを平坦化して保持
    train_texts = []
    train_labels = []

    for label_name, mails in label_data.items():
        for mail in mails.values():
            train_texts.append(make_text(mail))
            train_labels.append(label_name)

    # 新着メールの情報を取得
    new_ids = list(new_mail.keys())
    new_texts = [
        make_text(new_mail[mail_id])
        for mail_id in new_ids
    ]

    # TF-IDFで数値化
    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 4),
        lowercase=True,
    )

    train_vectors = vectorizer.fit_transform(train_texts)
    new_vectors = vectorizer.transform(new_texts)

    # 新着メールと教師データの類似度を算出
    similarities = cosine_similarity(
        new_vectors,
        train_vectors,
    )

    # メールごとにラベル別の平均類似度を計算
    judge_result = {}

    for i, mail_id in enumerate(new_ids):
        label_scores = {}

        for label_name in label_data:
            scores = [
                similarities[i][j]
                for j, train_label in enumerate(train_labels)
                if train_label == label_name
            ]

            label_scores[label_name] = (
                sum(scores) / len(scores) if scores else 0.0
            )

        judge_result[mail_id] = label_scores

    return judge_result