import random

# 花札のカードセット
CARDS = [
    (month, type_)
    for month in range(1, 13)  # 月（1月〜12月）
    for type_ in ["光", "短冊", "カス", "カス"]
]

def initialize_deck():
    """
    山札を生成してシャッフルする。
    :return: シャッフルされた山札
    """
    deck = CARDS.copy()
    random.shuffle(deck)
    return deck

def determine_parent(deck):
    """
    親を決定する。
    :param deck: シャッフル済み山札
    :return: 親、子
    """
    player_card = deck.pop()
    ai_card = deck.pop()

    print(f"プレイヤーのカード: {player_card[0]}月の{player_card[1]}")
    print(f"AIのカード: {ai_card[0]}月の{ai_card[1]}")

    if player_card[0] < ai_card[0]:
        print("プレイヤーが親です！")
        return "プレイヤー", "AI", deck
    else:
        print("AIが親です！")
        return "AI", "プレイヤー", deck

def deal_cards(deck):
    """
    カードを配布する。
    :param deck: シャッフル済み山札
    :return: プレイヤーの手札, AIの手札, 場札, 残りの山札
    """
    player_hand = []
    ai_hand = []
    field = []

    # 配布順序: 子→場→親
    for i in range(8):
        if i % 2 == 0:
            player_hand.append(deck.pop())  # 子
        else:
            ai_hand.append(deck.pop())  # 親
        field.append(deck.pop())  # 場札

    return player_hand, ai_hand, field, deck

# 初期化と親の決定テスト
deck = initialize_deck()
parent, child, deck = determine_parent(deck)
player_hand, ai_hand, field, deck = deal_cards(deck)

print("\n配布結果:")
print(f"プレイヤーの手札: {player_hand}")
print(f"AIの手札: {ai_hand}")
print(f"場札: {field}")
print(f"残り山札: {len(deck)}枚")
