# game/rules.py

from collections import Counter

def check_teyaku(hand):
    """
    手札に基づいて特別な役（手四、くっつき）を判定する。
    :param hand: プレイヤーの手札
    :return: 成立した役とスコア
    """
    teyaku = []
    score = 0

    # 手札を月ごとにグループ化
    month_counts = Counter(card.month for card in hand)

    # 手四の判定: 同じ月が4枚
    if any(count == 4 for count in month_counts.values()):
        teyaku.append("手四")
        score += 6

    # くっつきの判定: 同じ月が2枚ずつ4組
    pairs = sum(1 for count in month_counts.values() if count == 2)
    if pairs == 4:
        teyaku.append("くっつき")
        score += 6

    return teyaku, score


def check_yaku(cards):
    """
    役を判定してスコアを計算します。
    :param cards: プレイヤーの取得カードリスト
    :return: 成立した役とスコア
    """
    yaku = []
    score = 0

    # 種類別のカードをグループ化
    light_cards = [card for card in cards if card.type == "光"]
    ribbon_cards = [card for card in cards if card.type == "短冊"]
    seed_cards = [card for card in cards if card.type == "タネ"]
    junk_cards = [card for card in cards if card.type == "カス"]

    # 光札の役
    if len(light_cards) == 5:
        yaku.append("五光")
        score += 10
    elif len(light_cards) == 4 and any(card.name == "柳に小野道風" for card in light_cards):
        yaku.append("雨入り四光")
        score += 8
    elif len(light_cards) == 4:
        yaku.append("四光")
        score += 7
    elif len(light_cards) == 3:
        yaku.append("三光")
        score += 5

    # 短冊の役
    red_ribbons = [card for card in ribbon_cards if "赤" in card.name]
    blue_ribbons = [card for card in ribbon_cards if "青" in card.name]
    if len(red_ribbons) == 3:
        yaku.append("赤短")
        score += 5
    if len(blue_ribbons) == 3:
        yaku.append("青短")
        score += 5

    # タネの役
    animal_cards = [card for card in seed_cards if any(name in card.name for name in ["猪", "鹿", "蝶"])]
    if len(animal_cards) == 3:
        yaku.append("猪鹿蝶")
        score += 5

    # カス札の役
    if len(junk_cards) >= 10:
        yaku.append(f"カス{len(junk_cards)}枚")
        score += len(junk_cards) - 9  # 10枚で1点、以降1枚につき1点

    return yaku, score
