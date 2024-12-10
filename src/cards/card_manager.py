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
        special = "（カス得点）" if self.is_kasu_point else ""
        return f"{self.month}月の{self.category}{special}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.month == other.month and self.category == other.category


import random

class CardManager:
    def __init__(self):
        self.cards = []

    def initialize_cards(self):
        """
        花札のカードを初期化（48枚）
        """
        self.cards = [
            Card(1, "光"), Card(1, "短冊"), Card(1, "カス"), Card(1, "カス"),
            Card(2, "タネ"), Card(2, "短冊"), Card(2, "カス"), Card(2, "カス"),
            Card(3, "光"), Card(3, "短冊"), Card(3, "カス"), Card(3, "カス"),
            Card(4, "タネ"), Card(4, "短冊"), Card(4, "カス"), Card(4, "カス"),
            Card(5, "タネ"), Card(5, "短冊"), Card(5, "カス"), Card(5, "カス"),
            Card(6, "タネ"), Card(6, "短冊"), Card(6, "カス"), Card(6, "カス"),
            Card(7, "タネ"), Card(7, "短冊"), Card(7, "カス"), Card(7, "カス"),
            Card(8, "光"), Card(8, "タネ"), Card(8, "カス"), Card(8, "カス"),
            Card(9, "タネ"), Card(9, "短冊"), Card(9, "カス"), Card(9, "カス"),
            Card(10, "タネ"), Card(10, "短冊"), Card(10, "カス"), Card(10, "カス"),
            Card(11, "光"), Card(11, "カス"), Card(11, "カス"), Card(11, "カス"),
            Card(12, "光"), Card(12, "タネ"), Card(12, "カス"), Card(12, "カス"),
        ]

    def shuffle_deck(self):
        """
        山札をシャッフル
        """
        random.shuffle(self.cards)
    
    def draw_card(self):
        """
        山札からカードを1枚引く
        :return: Card オブジェクト
        """
        if not self.cards:
            raise ValueError("山札が空です！")
        return self.cards.pop()


    def check_roles(self, cards):
        """
        獲得したカードを基に役を判定する
        :param cards: 獲得したカードのリスト
        :return: 成立した役のリスト
        """
        if not isinstance(cards, list) or not all(isinstance(card, Card) for card in cards):
            raise ValueError("Invalid input: cards must be a list of Card objects")

        roles = []
        counts = {"光": 0, "タネ": 0, "短冊": 0, "カス": 0}
        special_sets = {"赤短": 0, "青短": 0}
        special_cards = {"猪": False, "鹿": False, "蝶": False}

        for card in cards:
            counts[card.category] += 1
            if card.month in [1, 2, 3] and card.category == "短冊":
                special_sets["赤短"] += 1
            elif card.month in [6, 9, 10] and card.category == "短冊":
                special_sets["青短"] += 1
            elif card.month == 7 and card.category == "タネ":
                special_cards["猪"] = True
            elif card.month == 10 and card.category == "タネ":
                special_cards["鹿"] = True
            elif card.month == 6 and card.category == "タネ":
                special_cards["蝶"] = True

        if counts["光"] == 5:
            roles.append("五光")
        elif counts["光"] == 4:
            roles.append("四光")
        elif counts["光"] == 3:
            roles.append("三光")

        if special_sets["赤短"] == 3 and special_sets["青短"] == 3:
            roles.append("赤短・青短の重複")
        else:
            if special_sets["赤短"] == 3:
                roles.append("赤短")
            if special_sets["青短"] == 3:
                roles.append("青短")

        if counts["短冊"] >= 5:
            roles.append(f"短冊（{counts['短冊']}枚）")
        if special_cards["猪"] and special_cards["鹿"] and special_cards["蝶"]:
            roles.append("猪鹿蝶")
        if counts["タネ"] >= 5:
            roles.append(f"タネ（{counts['タネ']}枚）")
        if counts["カス"] >= 10:
            roles.append(f"カス（{counts['カス']}枚）")

        return roles

    def calculate_points(self, roles):
        """
        成立した役から得点を計算する
        :param roles: 成立した役のリスト
        :return: 合計得点
        """
        points = 0
        role_points = {
            "五光": 10,
            "四光": 8,
            "三光": 5,
            "猪鹿蝶": 5,
            "赤短": 5,
            "青短": 5,
            "赤短・青短の重複": 10,
        }

        for role in roles:
            if role in role_points:
                points += role_points[role]
            elif "短冊" in role:
                count = int(role.split("（")[1][:-2])
                points += 1 + (count - 5)
            elif "タネ" in role:
                count = int(role.split("（")[1][:-2])
                points += 1 + (count - 5)
            elif "カス" in role:
                count = int(role.split("（")[1][:-2])
                points += 1 + (count - 10)

        return points
