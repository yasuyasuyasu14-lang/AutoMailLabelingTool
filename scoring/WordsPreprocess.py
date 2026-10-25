from janome.tokenizer import Tokenizer
import unicodedata

tokenizer = Tokenizer()

EXCLUDE_POS = {
    "助詞",
    "助動詞",
    "記号",
    "接続詞",
}

EXCLUDE_WORDS = {'re'}

import re
import html
from bs4 import BeautifulSoup

"""HTML・URLなどの不要情報を除去する"""
def _clean_text(text):

    text = html.unescape(str(text or ""))

    # URL除去
    text = re.sub(
        r"https?://[^\s<>\"']+",
        " ",
        text
    )

    # HTMLタグ・CSSなどを除去
    soup = BeautifulSoup(text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(" ")

    return text

def _is_symbol_only(text):
    return all(
        unicodedata.category(char)[0] in {"P", "S"}
        for char in text
    )

def _tokenize(text):
    """単語分割と不要語除去"""

    terms = []
    text = _clean_text(text).lower()

    for word in tokenizer.tokenize(str(text or "").lower()):

        term = word.surface
        pos = word.part_of_speech.split(",")[0]

        if (
            pos in EXCLUDE_POS
            or term in EXCLUDE_WORDS # 指定した単語を除外
            or len(term) <= 1 # 1文字以下の単語を除外
            or _is_symbol_only(term) # 記号のみの単語を除外
            or term.isnumeric() # 数字のみの単語を除外
        ):
            continue

        terms.append(term)

    return terms


def words_preprocess(source_data):
    """各ラベルのメール情報を前処理する"""

    preprocessed_data = {}

    for label_name, mails in source_data.items():

        preprocessed_data[label_name] = []

        for mail in mails:

            preprocessed_mail = {
                "id": mail.get("id", ""),
                "subject": _tokenize(mail.get("subject", "")),
                "body": _tokenize(mail.get("body", "")),
                "sender": mail.get("sender", ""),
                "category": mail.get("category", ""),
            }

            preprocessed_data[label_name].append(preprocessed_mail)

    return preprocessed_data