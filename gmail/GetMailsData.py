import base64
from datetime import datetime, timedelta, timezone

CATEGORY_MAP = {
    "CATEGORY_PURCHASES": "購入",
    "CATEGORY_SOCIAL": "ソーシャル",
    "CATEGORY_UPDATES": "新着",
    "CATEGORY_FORUMS": "フォーラム",
    "CATEGORY_PROMOTIONS": "プロモーション",
}

BATCH_SIZE = 100

"""指定ラベルのメール情報取得"""
def get_labeled_mails(g_service, label_names, limit):
    result = {}

    # 1. 指定ラベルごとに処理
    for label_name in label_names:
        label_id = _get_label_id(g_service, label_name)

        if not label_id:
            print(f"ラベル未検出: {label_name}")
            continue

        # このラベルのメール情報を格納するリスト
        result[label_name] = []

        messages = g_service.users().messages().list(
            userId="me",
            labelIds=[label_id],
            maxResults=limit
        ).execute().get("messages", [])

        # 2. このラベルのメールIDだけを格納
        tasks = [
            {
                "id": mail["id"],
                "answer_label": label_name,
            }
            for mail in messages
        ]

        # 3. このラベルのメールだけをバッチ化
        for start in range(0, len(tasks), BATCH_SIZE):
            chunk = tasks[start:start + BATCH_SIZE]
            responses = {}

            batch = g_service.new_batch_http_request()

            def make_callback(task):
                def callback(request_id, response, exception):
                    if exception:
                        print(
                            f"メール取得失敗: {task['id']}, "
                            f"エラー: {exception}"
                        )
                    else:
                        responses[request_id] = response

                return callback

            for index, task in enumerate(chunk):
                request = g_service.users().messages().get(
                    userId="me",
                    id=task["id"],
                    format="full",
                    fields="id,labelIds,payload"
                )

                batch.add(
                    request,
                    request_id=str(index),
                    callback=make_callback(task)
                )

            batch.execute()

            # 4. 取得結果をメール情報に変換
            for index, task in enumerate(chunk):
                detail = responses.get(str(index))

                if detail is None:
                    continue

                payload = detail.get("payload", {})
                headers = {
                    header["name"].lower(): header["value"]
                    for header in payload.get("headers", [])
                }

                categories = [
                    CATEGORY_MAP[label]
                    for label in detail.get("labelIds", [])
                    if label in CATEGORY_MAP
                ]

                result[label_name].append({
                    "id": task.get("id",""),
                    "subject": headers.get("subject", ""),
                    "body": _extract_body(payload),
                    "sender": headers.get("from", ""),
                    "category": categories[0] if categories else "未分類",
                })

    return result

"""新着メール情報取得（過去24時間以内の受信メール）"""
def get_new_mails(g_service):
    

    result = {"new": []}

    # ① 取得期間の設定
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=24)

    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())

    query = (
        f"after:{start_timestamp - 1} "
        f"before:{end_timestamp + 1}"
    )

    # ② メールIDを取得
    messages = []
    page_token = None

    while True:

        response = g_service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            q=query,
            maxResults=500,
            pageToken=page_token
        ).execute()

        messages.extend(response.get("messages", []))

        page_token = response.get("nextPageToken")

        if not page_token:
            break

    # ③ バッチ処理でメール詳細を取得
    for start in range(0, len(messages), BATCH_SIZE):

        chunk = messages[start:start + BATCH_SIZE]

        responses = {}

        batch = g_service.new_batch_http_request()

        def make_callback(mail_id):
            def callback(request_id, response, exception):

                if exception:
                    print(
                        f"メール取得失敗: {mail_id}, "
                        f"エラー: {exception}"
                    )
                else:
                    responses[request_id] = response

            return callback

        for index, mail in enumerate(chunk):

            request = g_service.users().messages().get(
                userId="me",
                id=mail["id"],
                format="full",
                fields="id,labelIds,internalDate,payload"
            )

            batch.add(
                request,
                request_id=str(index),
                callback=make_callback(mail["id"])
            )

        batch.execute()

        # ④ 取得結果を既存形式に変換
        for index, mail in enumerate(chunk):

            detail = responses.get(str(index))

            if detail is None:
                continue

            # 24時間以内かを厳密に確認
            received_time = int(detail["internalDate"]) / 1000

            if not (
                start_time.timestamp()
                <= received_time
                <= end_time.timestamp()
            ):
                continue

            payload = detail.get("payload", {})

            headers = {
                header["name"].lower(): header["value"]
                for header in payload.get("headers", [])
            }

            categories = [
                CATEGORY_MAP[label]
                for label in detail.get("labelIds", [])
                if label in CATEGORY_MAP
            ]

            result["new"].append({
                "id": detail.get("id", ""),
                "subject": headers.get("subject", ""),
                "body": _extract_body(payload),
                "sender": headers.get("from", ""),
                "category": categories[0] if categories else "未分類",
            })

    return result

def _extract_body(payload):
    """MIME構造から本文を取得する"""
    plain_text = None
    html_text = None

    def walk(part):
        nonlocal plain_text, html_text

        mime_type = part.get("mimeType", "")
        data = part.get("body", {}).get("data")

        if data:
            decoded = base64.urlsafe_b64decode(data).decode(
                "utf-8", errors="replace"
            )

            if mime_type == "text/plain" and plain_text is None:
                plain_text = decoded
            elif mime_type == "text/html" and html_text is None:
                html_text = decoded

        for child in part.get("parts", []):
            walk(child)

    walk(payload)
    return plain_text if plain_text is not None else (html_text or "")

def _get_label_id(g_service, label_name):
    labels = g_service.users().labels().list(
        userId='me'
    ).execute()
    for label in labels['labels']:
        if label['name'] == label_name:
            return label['id']
    return None