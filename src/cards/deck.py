# ファイル名: src/cards/deck.py

import random
import sys
import os

# プロジェクトルートからのパスを設定
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.cards.card import Card

class Deck:
    """
    山札を管理するクラス
    """
    def __init__(self):
        """
        48枚の花札を1組用意してシャッフル
        """
        self.cards = []  # 山札
        self.add_cards()  # 各月の札を追加
        random.shuffle(self.cards)  # シャッフル

    def add_cards(self):
        """
        各月の札を追加
        """
        self.cards.extend([
            # 1月: 松
            Card(1, "光"),       # 松に鶴
            Card(1, "短冊"),     # 松の短冊
            Card(1, "カス"),     # 松のカス1
            Card(1, "カス"),     # 松のカス2

            # 2月: 梅
            Card(2, "タネ"),     # 梅に鶯
            Card(2, "短冊"),     # 梅の短冊
            Card(2, "カス"),     # 梅のカス1
            Card(2, "カス"),     # 梅のカス2

            # 3月: 桜
            Card(3, "光"),       # 桜に幕
            Card(3, "短冊"),     # 桜の短冊
            Card(3, "カス"),     # 桜のカス1
            Card(3, "カス"),     # 桜のカス2

            # 4月: 藤
            Card(4, "タネ"),     # 藤にホトトギス
            Card(4, "短冊"),     # 藤の短冊
            Card(4, "カス"),     # 藤のカス1
            Card(4, "カス"),     # 藤のカス2

            # 5月: 牡丹
            Card(5, "タネ"),     # 牡丹に蝶
            Card(5, "短冊"),     # 牡丹の短冊
            Card(5, "カス"),     # 牡丹のカス1
            Card(5, "カス"),     # 牡丹のカス2

            # 6月: 菖蒲
            Card(6, "タネ"),     # 菖蒲に八橋
            Card(6, "青短"),     # 菖蒲の短冊
            Card(6, "カス"),     # 菖蒲のカス1
            Card(6, "カス"),     # 菖蒲のカス2

            # 7月: 萩
            Card(7, "タネ"),     # 萩に猪
            Card(7, "短冊"),     # 萩の短冊
            Card(7, "カス"),     # 萩のカス1
            Card(7, "カス"),     # 萩のカス2

            # 8月: 芒
            Card(8, "光"),       # 芒に月
            Card(8, "タネ"),     # 芒に雁
            Card(8, "カス"),     # 芒のカス1
            Card(8, "カス"),     # 芒のカス2

            # 9月: 菊
            Card(9, "タネ", is_kasu_point=True),  # 菊に盃
            Card(9, "短冊"),     # 菊の短冊
            Card(9, "カス"),     # 菊のカス1
            Card(9, "カス"),     # 菊のカス2

            # 10月: 紅葉
            Card(10, "タネ"),    # 紅葉に鹿
            Card(10, "短冊"),    # 紅葉の短冊
            Card(10, "カス"),    # 紅葉のカス1
            Card(10, "カス"),    # 紅葉のカス2

            # 11月: 柳
            Card(11, "光"),      # 雨入り光
            Card(11, "タネ"),    # 柳に燕
            Card(11, "カス"),    # 柳のカス1
            Card(11, "カス"),    # 柳のカス2

            # 12月: 桐
            Card(12, "光"),      # 桐に鳳凰
            Card(12, "カス"),    # 桐のカス1
            Card(12, "カス"),    # 桐のカス2
            Card(12, "カス")     # 桐のカス3
        ])

    def draw(self):
        """
        山札からカードを1枚引く
        :return: Card オブジェクト
        """
        if not self.cards:
            raise ValueError("山札が空です！")
        return self.cards.pop()

    def __len__(self):
        """
        山札の残り枚数を返す
        """
        return len(self.cards)

    def show_deck(self):
        """
        現在の山札を表示（デバッグ用）
        """
        for card in self.cards:
            print(card)

# テストコード
if __name__ == "__main__":
    deck = Deck()
    print(f"山札の枚数: {len(deck)}枚")  # 正しく48枚になるはず
    deck.show_deck()  # 山札の中身を確認
    drawn_card = deck.draw()
    print(f"引いたカード: {drawn_card}")
    print(f"山札の残り枚数: {len(deck)}枚")
