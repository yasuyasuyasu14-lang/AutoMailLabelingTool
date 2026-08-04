import config

class GmailMessage:
    def __init__(self, msg: dict):
        # 基本情報取得
        self.id = msg.get('id')
        self.thread_id = msg.get('threadId')
        self.labels = msg.get('labelIds', [])
        self.snippet = msg.get('snippet')

        # ヘッダ経情報取得
        payload = msg.get('payload', {})
        headers = payload.get('headers', [])
        self.is_attachment = self._is_attachment(payload)
        self.from_ = self._get_header(headers, 'From')
        self.to = self._get_header(headers, 'To')
        self.cc = self._get_header(headers, 'Cc')
        self.subject = self._get_header(headers, 'Subject')
        self.date = self._get_header(headers, 'Date')
        # 本文
        # self.body = self._extract_body(payload)

    # ------------------------
    # 便利メソッド（今後使う）
    # ------------------------
    def calc_labels(self):
        for label in self.labels:
            score = config.LABEL_SCORES.get(label)
            if score is not None:
                self._calculation(f"ラベル_{label}", score)
        
        self.score = 0
        self.judg = []
        # --- ラベル ---
        if "SENT" in self.labels:
            self._calculation("ラベル_送信",10)
        if "STARRED" in self.labels:
            self._calculation("ラベル_スター",10)
        if "UNREAD" in self.labels:
            self._calculation("ラベル_未読",-3)
        if "INBOX" in self.labels:
            self._calculation("ラベル_アーカイブ",5)
        if "DRAFT" in self.labels:
            self._calculation("ラベル_下書き",3)
        if "TRASH" in self.labels:
            self._calculation("ラベル_ゴミ箱",-5)
        if "SPAM" in self.labels:
            self._calculation("ラベル_スパム",-10)
        if "IMPORTANT" in self.labels:
            self._calculation("ラベル_重要",5)
        if "CATEGORY_PERSONAL" in self.labels:
            self._calculation("ラベル_個人宛",3)
        if "CATEGORY_UPDATES" in self.labels:
            self._calculation("ラベル_自動通知",-3)
        if "CATEGORY_PROMOTIONS" in self.labels:
            self._calculation("ラベル_プロモ",-3)
        if "CATEGORY_SOCIAL" in self.labels:
            self._calculation("ラベル_ソーシャル",-3)
        if "CATEGORY_FORUMS" in self.labels:
            self._calculation("ラベル_一括通知",-3)

        # --- 宛先 ---
        if self._is_direct():
            self._calculation("宛先_direct",10)
        if self._is_cc():
            self._calculation("宛先_cc",-5)

        # --- その他 ---
        if self.is_attachment:
            self._calculation("その他_添付",10)

        # --- 件名キーワード ---

    # ------------------------
    # 内部メソッド
    # ------------------------

    def _is_attachment(self,payload):
            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('filename'):
                        return True
            return False

    def _get_header(self, headers, name):
        for h in headers:
            if h['name'] == name:
                return h['value']
        return None

    def _is_cc(self):
        return self.cc is not None

    def _is_direct(self):
        return self.to is not None and self.cc is None

    def _calculation(self, reason, delta):
        self.score += delta
        self.judg.append({"reason": reason,"score": delta})

    def __repr__(self):
        return f"<GmailMessage subject={self.subject} from={self.from_}>"