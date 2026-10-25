from sklearn.feature_extraction.text import TfidfVectorizer


def get_tfidf_feature(preprocessed_data):
    """件名・本文のラベル別平均TF-IDFを取得"""

    subjects = []
    bodies = []
    document_labels = []

    subject_features = {
        label_name: {}
        for label_name in preprocessed_data
    }

    body_features = {
        label_name: {}
        for label_name in preprocessed_data
    }

    # ① 全メールの件名・本文を収集
    for label_name, mails in preprocessed_data.items():

        for mail in mails:

            subjects.append(" ".join(mail["subject"]))
            bodies.append(" ".join(mail["body"]))

            document_labels.append(label_name)

    # ② データが存在しない場合
    if not subjects or not any(subjects + bodies):
        return subject_features, body_features, None

    # ③ 全メール共通のTF-IDFを学習
    vectorizer = TfidfVectorizer(
        tokenizer=str.split,
        token_pattern=None,
        lowercase=False,
    )

    vectorizer.fit(subjects + bodies)

    # ④ 件名・本文を別々にベクトル化
    subject_matrix = vectorizer.transform(subjects)
    body_matrix = vectorizer.transform(bodies)

    feature_names = vectorizer.get_feature_names_out()

    # ⑤ ラベルごとの平均特徴量を取得
    for label_name in preprocessed_data:

        indices = [
            i for i, label in enumerate(document_labels)
            if label == label_name
        ]

        if not indices:
            continue

        subject_weights = subject_matrix[indices].mean(axis=0).A1
        body_weights = body_matrix[indices].mean(axis=0).A1

        subject_features[label_name] = {
            term: float(weight)
            for term, weight in zip(feature_names, subject_weights)
            if weight > 0
        }

        body_features[label_name] = {
            term: float(weight)
            for term, weight in zip(feature_names, body_weights)
            if weight > 0
        }

    return subject_features, body_features, vectorizer