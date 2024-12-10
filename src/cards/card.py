# ファイル名: src/cards/card.py

class Card:
    """
    花札のカードを表現するクラス
    """
    def __init__(self, month, category, is_kasu_point=False):
        """
        :param month: 月（1～12の整数）
        :param category: 種類（"光", "短冊", "タネ", "カス"）
        :param is_kasu_point: カス得点としても計算される場合に True
        """
        self.month = month
        self.category = category
        self.is_kasu_point = is_kasu_point

    def __repr__(self):
        """
        カードの文字列表現
        """
        special = "（カス得点）" if self.is_kasu_point else ""
        return f"{self.month}月の{self.category}{special}"

    def __eq__(self, other):
        """
        カード同士の比較（同じ月と種類の場合に等しいとみなす）
        """
        return self.month == other.month and self.category == other.category
