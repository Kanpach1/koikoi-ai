# src/utils/display.py

def display_hand(player, hand):
    """
    プレイヤーの手札を表示する。
    """
    print(f"=== {player}の手札 ===")
    for i, card in enumerate(hand):
        print(f"[{i}] {card[0]}の{card[1]}")
    print("===================")


def display_field(field, deck_size):
    """
    場札と山札の状況を表示する。
    """
    print("=== 場札 ===")
    for card in field:
        print(f"{card[0]}の{card[1]}")
    print("===================")
    print(f"山札の残り枚数: {deck_size}")
    print()


def display_scores(scores):
    """
    プレイヤーとAIの得点を表示する。
    """
    print("=== 得点 ===")
    for player, score in scores.items():
        print(f"{player}: {score}点")
    print("===================")


def display_turn_info(player):
    """
    現在のターンの情報を表示する。
    """
    print(f"現在のターン: {player}")
    print("===================")

# テストデータ
test_hand = [("1月", "光"), ("2月", "短冊"), ("3月", "カス")]
test_field = [("4月", "短冊"), ("5月", "カス")]
test_scores = {"プレイヤー": 5, "AI": 8}
test_turn_player = "プレイヤー"

# テスト表示
display_hand("プレイヤー", test_hand)
display_field(test_field, 20)
display_scores(test_scores)
display_turn_info(test_turn_player)
