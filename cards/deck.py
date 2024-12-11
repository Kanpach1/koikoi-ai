# cards/deck.py

import random
from cards.card import create_deck

class Deck:
    """
    花札のデッキを管理するクラス。
    """
    def __init__(self):
        self.cards = create_deck()  # デッキを生成
        self.field = []  # 場のカード
        self.parent_hand = []  # 親の手札
        self.child_hand = []  # 子の手札
        self.remaining_deck = []  # 山札
        self.deal_order = []  # 配布順序を記録

    def shuffle(self):
        """
        デッキをシャッフルする。
        """
        random.shuffle(self.cards)

    def deal(self):
        """
        手札と場にカードを配る。
        配布順序を記録する。
        """
        for _ in range(8):
            child_card = self.cards.pop(0)  # 子の手札
            field_card = self.cards.pop(0)  # 場のカード
            parent_card = self.cards.pop(0)  # 親の手札

            self.child_hand.append(child_card)
            self.field.append(field_card)
            self.parent_hand.append(parent_card)

            # 配布順序を記録
            self.deal_order.extend([child_card, field_card, parent_card])

        # 配布後の残りカードを山札に設定
        self.remaining_deck = self.cards[:]

    def show_hands(self):
        """
        手札と場の状態を表示する（デバッグ用）。
        """
        print("子の手札（裏向け）:")
        print(["[裏]" for _ in self.child_hand])
        print("\n場（表向け）:")
        print(self.field)
        print("\n親の手札（裏向け）:")
        print(["[裏]" for _ in self.parent_hand])

    def draw_card(self):
        """
        山札から1枚引く。
        :return: 山札から引いたカード。
        """
        return self.remaining_deck.pop(0) if self.remaining_deck else None
