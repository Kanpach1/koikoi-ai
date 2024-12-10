# ファイル名: src/game/score.py
import sys
import os

# プロジェクトルートをモジュール検索パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.cards.card import Card


class ScoreCalculator:
    """
    役判定と得点計算を行うクラス
    """
    def __init__(self):
        pass

    @staticmethod
    def check_roles(cards):
        """
        獲得したカードを基に役を判定する
        :param cards: 獲得したカードのリスト
        :return: 成立した役のリスト
        """
        if not isinstance(cards, list) or not all(isinstance(card, Card) for card in cards):
            raise ValueError("カードリストが無効です。Cardオブジェクトのリストを渡してください。")

        roles = []
        counts = {"光": 0, "タネ": 0, "短冊": 0, "カス": 0}
        special_cards = {"猪": False, "鹿": False, "蝶": False, "酒": False, "桜": False, "月": False}

        for card in cards:
            counts[card.category] += 1
            if card.month == 7 and card.category == "タネ":
                special_cards["猪"] = True
            elif card.month == 10 and card.category == "タネ":
                special_cards["鹿"] = True
            elif card.month == 6 and card.category == "タネ":
                special_cards["蝶"] = True
            elif card.month == 9 and card.category == "タネ":
                special_cards["酒"] = True
            elif card.month == 3 and card.category == "光":
                special_cards["桜"] = True
            elif card.month == 8 and card.category == "光":
                special_cards["月"] = True

        if counts["光"] == 5:
            roles.append("五光")
        elif counts["光"] == 4:
            roles.append("四光")
        elif counts["光"] == 3:
            rain_card = any(card.month == 11 and card.category == "光" for card in cards)
            if not rain_card:
                roles.append("三光")

        if special_cards["猪"] and special_cards["鹿"] and special_cards["蝶"]:
            roles.append("猪鹿蝶")

        if special_cards["桜"] and special_cards["酒"]:
            roles.append("花見酒")

        return roles

    @staticmethod
    def calculate_points(roles):
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
            "花見酒": 5
        }

        for role in roles:
            if role in role_points:
                points += role_points[role]
        return points
