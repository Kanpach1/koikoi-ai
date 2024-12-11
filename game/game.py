# game/game.py

from game.rules import check_teyaku, check_yaku

class Game:
    def __init__(self, deck):
        """
        ゲームの初期化
        :param deck: シャッフルされたデッキ
        """
        self.deck = deck
        self.parent = None
        self.child = None

    def determine_parent(self):
        """
        親を決定する。
        山札のカードを1枚ずつめくり、月の早いほうが親となる。
        """
        print("親を決定します...")
        while True:
            # 親候補カードを山札から1枚ずつ引く
            candidate1 = self.deck.draw_card()
            candidate2 = self.deck.draw_card()

            print(f"候補1: {candidate1}, 候補2: {candidate2}")

            # 月の早いほうが親
            if candidate1.month < candidate2.month:
                self.parent = "親"
                self.child = "子"
                print("親が決定: 親は候補1のプレイヤーです")
                return
            elif candidate1.month > candidate2.month:
                self.parent = "子"
                self.child = "親"
                print("親が決定: 親は候補2のプレイヤーです")
                return
            else:
                print("引き分け！もう一度カードを引きます。")

    def evaluate_teyaku(self, player_name, hand):
        """
        プレイヤーの手札役（手四、くっつき）を判定し、得点を計算する。
        :param player_name: プレイヤーの名前
        :param hand: プレイヤーの手札
        :return: 成立した役とスコア
        """
        teyaku, score = check_teyaku(hand)
        if teyaku:
            print(f"{player_name} の手札役: {teyaku}")
            print(f"{player_name} のスコア: {score} 点")
        return teyaku, score

    def play(self):
        """
        ゲームを進行します。
        """
        print("ゲーム開始！")

        # 配布されたカードを表示
        self.deck.show_hands()

        # 親を決定
        self.determine_parent()

        # 親と子の手札役判定
        parent_teyaku, parent_score = self.evaluate_teyaku("親", self.deck.parent_hand)
        child_teyaku, child_score = self.evaluate_teyaku("子", self.deck.child_hand)

        # 手札役が成立した場合は次の回へ
        if parent_teyaku or child_teyaku:
            if parent_teyaku:
                print("親の手札役が成立！次の回に進みます。")
            if child_teyaku:
                print("子の手札役が成立！次の回に進みます。")
            return

        # 手札役が成立しない場合、通常の役判定へ進む
        print("\n手札役はありません。通常の役判定へ進みます。")
        parent_yaku, parent_score = check_yaku(self.deck.parent_hand)
        child_yaku, child_score = check_yaku(self.deck.child_hand)

        # 勝敗判定
        if parent_score > child_score:
            print("親の勝利！")
        elif parent_score < child_score:
            print("子の勝利！")
        else:
            print("引き分け！")
