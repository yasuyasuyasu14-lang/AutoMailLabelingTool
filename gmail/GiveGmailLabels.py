
"""最大類似度が閾値以上のメールにラベルを付与する"""
def give_gmail_labels(g_service, total_scores, threshold):
    # ① Gmailのラベル名とIDの対応を取得
    response = g_service.users().labels().list(
        userId="me"
    ).execute()

    label_ids = {
        label["name"]: label["id"]
        for label in response.get("labels", [])
    }

    # ② メールごとに判定
    for mail_id, scores in total_scores.items():

        if not scores:
            continue

        # 最も類似度が高いラベルを取得
        best_label = max(scores, key=scores.get)
        best_score = scores[best_label]

        # ③ 閾値未満ならスキップ
        if best_score < threshold:
            print(
                f"スキップ: {mail_id} "
                f"(最大類似度: {best_score:.4f})"
            )
            continue

        # ④ ラベルIDを取得
        label_id = label_ids.get(best_label)

        if not label_id:
            print(f"ラベル未検出: {best_label}")
            continue

        # ⑤ Gmailにラベルを付与
        try:
            """
            g_service.users().messages().modify(
                userId="me",
                id=mail_id,
                body={
                    "addLabelIds": [label_id]
                }
            ).execute()
            """

            print(
                f"ラベル付与: {mail_id} → {best_label} "
                f"(類似度: {best_score:.4f})"
            )

        except Exception as e:
            print(
                f"ラベル付与失敗: {mail_id}, "
                f"エラー: {e}"
            )