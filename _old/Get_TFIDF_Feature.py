from sklearn.feature_extraction.text import TfidfVectorizer

def Get_tfidf_Feature(preprocessed_data):
    """全メール共通のTF-IDFからラベル別の平均特徴量を算出"""

    documents = []
    document_labels = []

    features = {
        label_name: {}
        for label_name in preprocessed_data
    }

    # ① 全ラベルのメールを収集
    for label_name, mails in preprocessed_data.items():

        for mail in mails:

            terms = mail["subject"] + mail["body"]

            documents.append(" ".join(terms))
            document_labels.append(label_name)

    # ② データが存在しない場合
    if not documents or not any(documents):
        return features

    # ③ 全メール共通のTF-IDF計算
    vectorizer = TfidfVectorizer(
        tokenizer=str.split,
        token_pattern=None,
        lowercase=False,
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    feature_names = vectorizer.get_feature_names_out()

    # ④ ラベルごとに平均TF-IDFを算出
    for label_name in preprocessed_data:

        indices = [
            i for i, label in enumerate(document_labels)
            if label == label_name
        ]

        if not indices:
            continue

        mean_weights = (
            tfidf_matrix[indices].mean(axis=0).A1
        )

        features[label_name] = {
            term: float(weight)
            for term, weight in zip(
                feature_names,
                mean_weights
            )
            if weight > 0
        }

    return features