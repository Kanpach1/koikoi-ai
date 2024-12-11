# tests/test_deck.py

import unittest
from cards.deck import Deck

class TestDeck(unittest.TestCase):
    def setUp(self):
        """
        各テストの前に新しいデッキを準備します。
        """
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.deal()

    def test_card_counts(self):
        """
        手札、場、山札のカード数が正しいことを確認。
        """
        # 手札（親と子）が8枚ずつ
        self.assertEqual(len(self.deck.child_hand), 8, "子の手札が8枚ではありません")
        self.assertEqual(len(self.deck.parent_hand), 8, "親の手札が8枚ではありません")
        
        # 場が8枚
        self.assertEqual(len(self.deck.field), 8, "場のカードが8枚ではありません")

        # 山札のカード数 = 総カード数 - 配布済みカード数
        remaining_cards = 48 - (8 + 8 + 8)
        self.assertEqual(
            len(self.deck.remaining_deck), 
            remaining_cards, 
            "山札のカード数が正しくありません"
        )

    def test_no_duplicate_cards(self):
        """
        配布されたカードに重複がないことを確認。
        """
        # 全てのカードを一つのリストにまとめる
        all_cards = self.deck.child_hand + self.deck.parent_hand + self.deck.field + self.deck.remaining_deck

        # 重複がないことを確認
        self.assertEqual(
            len(all_cards), len(set(all_cards)), 
            "カードに重複があります"
        )

    def test_distribution_order(self):
        """
        配布が子→場→親の順に行われていることを確認。
        """
        # 実際の配布順序を取得
        actual_deal_order = self.deck.deal_order

        # 配布された順序を再現
        expected_order = []
        for i in range(8):
            expected_order.append(self.deck.child_hand[i])
            expected_order.append(self.deck.field[i])
            expected_order.append(self.deck.parent_hand[i])

        self.assertEqual(
            actual_deal_order, 
            expected_order, 
            "配布順序が正しくありません"
        )


if __name__ == "__main__":
    unittest.main()
