# ファイル名: src/game/game_manager.py

import sys
import os

# プロジェクトルートをモジュール検索パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import random
from src.cards.deck import Deck



class GameManager:
    """
    ゲーム進行全体を管理するクラス
    """
    def __init__(self):
        self.deck = Deck()  # 山札を生成
        self.player_hands = {"player": [], "ai": []}  # 各プレイヤーの手札
        self.field_cards = []  # 場札
        self.player_acquired = {"player": [], "ai": []}  # 獲得札
        self.scores = {"player": 0, "ai": 0}  # スコア
        self.round_count = 1  # 現在のラウンド数

    def initialize_game(self):
        """
        ゲームの初期化処理
        """
        self.deck = Deck()  # 新しい山札を生成
        self.field_cards = []  # 場札を初期化
        self.player_hands = {"player": [], "ai": []}  # 手札を初期化
        self.player_acquired = {"player": [], "ai": []}  # 獲得札を初期化
        self.scores = {"player": 0, "ai": 0}  # スコアを初期化

        # 山札からカードを配る
        self.deal_cards()

    def deal_cards(self):
        """
        山札から手札と場札を配る
        """
        for _ in range(8):
            self.player_hands["player"].append(self.deck.draw())
            self.player_hands["ai"].append(self.deck.draw())
            self.field_cards.append(self.deck.draw())

    def play_turn(self, player):
        """
        1ターンの進行
        :param player: "player" または "ai"
        """
        # 手札からカードを場に出す
        selected_card = self.player_hands[player].pop(random.randint(0, len(self.player_hands[player]) - 1))
        print(f"{player}が出したカード: {selected_card}")

        # 場札と合札を確認
        matching_cards = [card for card in self.field_cards if card.month == selected_card.month]
        if matching_cards:
            # 合札の場合
            acquired_card = matching_cards.pop(0)  # 場札から1枚取得
            self.field_cards.remove(acquired_card)
            self.player_acquired[player].extend([selected_card, acquired_card])
            print(f"{player}が合札を獲得: {selected_card}, {acquired_card}")
        else:
            # 合札がない場合
            self.field_cards.append(selected_card)
            print(f"{player}は合札がなく、カードを場に追加: {selected_card}")

        # 山札からカードを引く
        drawn_card = self.deck.draw()
        print(f"{player}が山札から引いたカード: {drawn_card}")
        matching_cards = [card for card in self.field_cards if card.month == drawn_card.month]
        if matching_cards:
            # 合札の場合
            acquired_card = matching_cards.pop(0)
            self.field_cards.remove(acquired_card)
            self.player_acquired[player].extend([drawn_card, acquired_card])
            print(f"{player}が山札から合札を獲得: {drawn_card}, {acquired_card}")
        else:
            # 合札がない場合
            self.field_cards.append(drawn_card)
            print(f"{player}は山札からの合札がなく、カードを場に追加: {drawn_card}")

    def check_roles(self, player):
        """
        プレイヤーの役を確認して得点を加算
        """
        # 獲得したカードで役を判定し、スコアに加算
        pass  # 実装予定

    def end_game(self):
        """
        ゲーム終了後の処理
        """
        print("ゲーム終了！最終スコア:")
        print(f"プレイヤー: {self.scores['player']}点")
        print(f"AI: {self.scores['ai']}点")

# テストコード
if __name__ == "__main__":
    manager = GameManager()
    manager.initialize_game()
    print(f"プレイヤーの手札: {manager.player_hands['player']}")
    print(f"AIの手札: {manager.player_hands['ai']}")
    print(f"場札: {manager.field_cards}")

    # テスト: 1ターン進行
    manager.play_turn("player")
    manager.play_turn("ai")
