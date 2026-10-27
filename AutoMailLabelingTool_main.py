# main.py
import config
import logging
# ログの初期設定
logging.basicConfig(
level=logging.INFO,
format="[%(asctime)s] [%(levelname)s] %(message)s",
datefmt="%H:%M:%S")

from gmail.GetGmailService import get_gmail_service
from gmail.GetMailsData import get_labeled_mails
from gmail.GetMailsData import get_new_mails
from gmail.GiveGmailLabels import give_gmail_labels
from scoring.WordsPreprocess import words_preprocess
from scoring.GetTfidfFeature import get_tfidf_feature
from scoring.GetCategoryFeature import get_category_feature
from scoring.GetSenderFeature import get_sender_feature
from scoring.GetNewFeature import get_new_feature
from similarity.CalcParamSimilarity import calc_param_similarity
from similarity.CalcTotalSimilarity import calc_total_similarity

print("==================== Auto Mail Labeling Tool ====================")

if __name__ == "__main__":
    logging.info("---------- 処理を開始しました ----------")
    # --- GmailAPI認証 ---
    logging.info("Gmail APIへの接続中...")
    g_service = get_gmail_service(scopes=config.SCOPES)

    # ===== 指定ラベルのメール情報取得 =====
    logging.info("---------- 各指定ラベルメールの特徴量算出 ----------")
    logging.info("メール情報を取得中...")
    source_data = get_labeled_mails(g_service,
        label_names=config.LABEL_NAMES,
        limit=config.DEFAULT_GET_LIMIT)

    # 単語分割/前処理
    logging.info("前処理を実行中...")
    processed_data = words_preprocess(source_data)

    # TF-IDF特徴量の計算
    logging.info("TF-IDFによる特徴量を計算中...")
    subject_ft, body_ft, vectorizer  = get_tfidf_feature(processed_data)

    # カテゴリ特徴量の計算
    logging.info("各メールカテゴリの特徴量を計算中...")
    category_ft = get_category_feature(processed_data)

    # 送信者特徴量の計算
    logging.info("各メール送信者の特徴量を計算中...")
    sender_ft = get_sender_feature(processed_data,
        domain_weight=config.DOMAIN_WEIGHT)

    # ラベルごとの各特徴量を統合
    label_features = {}
    for label_name in subject_ft:
        label_features[label_name] = {
            "subject": subject_ft[label_name],
            "body": body_ft[label_name],
            "sender": sender_ft[label_name],
            "category": category_ft[label_name]}

    # ===== 新着メール情報取得 =====
    logging.info("---------- 新着メールの特徴量算出 ----------")
    logging.info("メール情報を取得中...")
    source_data_new = get_new_mails(g_service)

    # 単語分割/前処理
    logging.info("前処理を実行中...")
    processed_data = words_preprocess(source_data_new)

    # 特徴量計算
    logging.info("特徴量を計算中...")
    new_features = get_new_feature(
        processed_data["new"],
        vectorizer)

    # ===== 類似度計算 =====
    logging.info("類似度を計算中...")
    similarities = calc_param_similarity(
        label_features,
        new_features)

    # ===== 総合スコア計算 =====
    logging.info("総合スコアを計算中...")
    total_scores = calc_total_similarity(
        similarities,
        config.FEATURE_WEIGHT)

    # ===== Gmailへのラベル付与 =====
    give_gmail_labels(
        g_service,
        total_scores,
        threshold=config.LABEL_THRESHOLD)
aaa


# DBの使用方法の理解
# カラム名：ラベル名として各判定メールIDを羅列する形？


