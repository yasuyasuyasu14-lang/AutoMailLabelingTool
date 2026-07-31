class GmailMessage:
    def __init__(self, raw_msg: dict):
        # 基本情報取得
        self.id = raw_msg.get('id')
        self.thread_id = raw_msg.get('threadId')
        self.label_ids = raw_msg.get('labelIds', [])
        self.snippet = raw_msg.get('snippet')

        # ヘッダ経情報取得
        payload = raw_msg.get('payload', {})
        headers = payload.get('headers', [])
        self.from_ = self._get_header(headers, 'From')
        self.to = self._get_header(headers, 'To')
        self.cc = self._get_header(headers, 'Cc')
        self.subject = self._get_header(headers, 'Subject')
        self.date = self._get_header(headers, 'Date')
        # 本文
        # self.body = self._extract_body(payload)

    # ------------------------
    # 内部メソッド
    # ------------------------

    def _get_header(self, headers, name):
        for h in headers:
            if h['name'] == name:
                return h['value']
        return None

    # ------------------------
    # 便利メソッド（今後使う）
    # ------------------------
    def calc_score(self):
        score = 0
        judg = []
        # --- ラベル ---
        if self._is_important():
            score += 5
            judg.append(("ラベル_IMPORTANT", 5))
        if self._is_promotion():
            score -= 5
            judg.append(("ラベル_PROMOTIONS", 5))
        if self._is_social():
            score -= 3
            judg.append(("ラベル_SOCIAL", -3))
        # --- 件名キーワード ---
        if self.subject:
            if "緊急" in self.subject:
                score += 4
            if "至急" in self.subject:
                score += 4
            if "お知らせ" in self.subject:
                score -= 2
        # --- 宛先 ---
        if self._is_direct():
            score += 3
            judg.append(("宛先_only to", +3))
        if self._is_cc():
            score -= 2
            judg.append(("宛先_cc", -2))
        return score,judg

    def _is_important(self):
        return 'IMPORTANT' in self.label_ids

    def _is_promotion(self):
        return 'CATEGORY_PROMOTIONS' in self.label_ids

    def _is_social(self):
        return 'CATEGORY_SOCIAL' in self.label_ids

    def has_attachment(self):
        payload = self.raw.get('payload', {})
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    return True
        return False

    def _is_cc(self):
        return self.cc is not None

    def _is_direct(self):
        return self.to is not None and self.cc is None

    def __repr__(self):
        return f"<GmailMessage subject={self.subject} from={self.from_}>"