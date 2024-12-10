import sys
import os

# プロジェクトルートをモジュール検索パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.game.score import ScoreCalculator
from src.cards.card import Card

def test_roles():
    """
    役判定のテスト
    """
    test_cases = [
        # 五光
        {
            "name": "五光",
            "cards": [
                Card(1, "光"), Card(3, "光"), Card(8, "光"),
                Card(11, "光"), Card(12, "光")
            ],
            "expected_roles": ["五光"],
            "expected_points": 10
        },
        # 四光
        {
            "name": "四光",
            "cards": [
                Card(1, "光"), Card(3, "光"), Card(8, "光"),
                Card(12, "光")
            ],
            "expected_roles": ["四光"],
            "expected_points": 8
        },
        # 三光
        {
            "name": "三光",
            "cards": [
                Card(1, "光"), Card(3, "光"), Card(8, "光")
            ],
            "expected_roles": ["三光"],
            "expected_points": 5
        },
        # 猪鹿蝶
        {
            "name": "猪鹿蝶",
            "cards": [
                Card(7, "タネ"), Card(10, "タネ"), Card(6, "タネ")
            ],
            "expected_roles": ["猪鹿蝶"],
            "expected_points": 5
        },
        # 花見で一杯
        {
            "name": "花見で一杯",
            "cards": [
                Card(3, "光"), Card(9, "タネ")
            ],
            "expected_roles": ["花見で一杯"],
            "expected_points": 5
        },
        # 月見で一杯
        {
            "name": "月見で一杯",
            "cards": [
                Card(8, "光"), Card(9, "タネ")
            ],
            "expected_roles": ["月見で一杯"],
            "expected_points": 5
        },
        # 短冊
        {
            "name": "短冊",
            "cards": [
                Card(1, "短冊"), Card(2, "短冊"), Card(3, "短冊"),
                Card(4, "短冊"), Card(5, "短冊")
            ],
            "expected_roles": ["短冊（5枚）"],
            "expected_points": 1
        },
        # タネ
        {
            "name": "タネ",
            "cards": [
                Card(2, "タネ"), Card(4, "タネ"), Card(5, "タネ"),
                Card(6, "タネ"), Card(7, "タネ")
            ],
            "expected_roles": ["タネ（5枚）"],
            "expected_points": 1
        },
        # カス
        {
            "name": "カス",
            "cards": [
                Card(1, "カス"), Card(2, "カス"), Card(3, "カス"),
                Card(4, "カス"), Card(5, "カス"),
                Card(6, "カス"), Card(7, "カス"), Card(8, "カス"),
                Card(9, "カス"), Card(10, "カス")
            ],
            "expected_roles": ["カス（10枚）"],
            "expected_points": 1
        }
    ]

    for case in test_cases:
        roles = ScoreCalculator.check_roles(case["cards"])
        points = ScoreCalculator.calculate_points(roles)
        assert roles == case["expected_roles"], f"Test failed for {case['name']}: Expected roles {case['expected_roles']}, got {roles}"
        assert points == case["expected_points"], f"Test failed for {case['name']}: Expected points {case['expected_points']}, got {points}"
        print(f"Test passed for {case['name']}")

if __name__ == "__main__":
    test_roles()
