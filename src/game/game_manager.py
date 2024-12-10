import sys
import os
import logging
from src.cards.card_manager import CardManager
from rich.console import Console
from rich.table import Table
from rich.box import SIMPLE, ROUNDED

console = Console()


class GameManager:
    def __init__(self, player1, player2):
        """
        ゲームマネージャーの初期化
        :param player1: プレイヤー1（AIまたはユーザー）
        :param player2: プレイヤー2（AIまたはユーザー）
        """
        self.player1 = player1
        self.player2 = player2
        self.card_manager = CardManager()
        self.round_number = 0
        self.current_turn = 0  # ラウンド内のターン数を管理
        self.players = {"AI1": [], "AI2": []}  # プレイヤーの手札
        self.scores = {"AI1": 0, "AI2": 0}  # 各プレイヤーのスコア
        self.field = []  # 場のカード
        self.acquired = {"AI1": {"光": [], "タネ": [], "短冊": [], "カス": []},
                         "AI2": {"光": [], "タネ": [], "短冊": [], "カス": []}}

        # ログの初期化
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    def initialize_game(self):
        """
        ゲームを初期化
        """
        self.card_manager.initialize_cards()  # カードを初期化
        self.card_manager.shuffle_deck()  # デッキをシャッフル
        logging.info("ゲームを初期化しました。山札をシャッフルしました。")

        # 各プレイヤーと場にカードを配布
        for player in self.players:
            self.players[player] = [self.card_manager.draw_card() for _ in range(8)]
        self.field = [self.card_manager.draw_card() for _ in range(8)]

        console.print("[bold cyan]=== ゲーム開始 ===[/bold cyan]")
        self.display_game_state()

    def display_game_state(self):
        """
        現在のゲーム状態をコンソールに表示する
        """
        # プレイヤーの手札を表示
        hand_table = Table(title="Players' Hands", box=ROUNDED)
        hand_table.add_column("Player", justify="center", style="cyan")
        hand_table.add_column("Hand", justify="center", style="green")

        for player, hand in self.players.items():
            hand_table.add_row(player, ", ".join(map(str, hand)))

        console.print(hand_table)

        # 場のカードを表示
        field_table = Table(title="Field Cards", box=ROUNDED)
        field_table.add_column("Cards", justify="center", style="yellow")
        field_table.add_row(", ".join(map(str, self.field)))

        console.print(field_table)

        # 獲得札を表示
        for player, cards in self.acquired.items():
            acquired_table = Table(title=f"{player}'s Acquired Cards", box=SIMPLE)
            acquired_table.add_column("Category", justify="center", style="magenta")
            acquired_table.add_column("Cards", justify="center", style="green")

            for category, card_list in cards.items():
                acquired_table.add_row(category, ", ".join(map(str, card_list)))

            console.print(acquired_table)

    def play_turn(self, player):
        """
        プレイヤーのターン処理
        """
        self.current_turn += 1  # ターン数を更新
        console.print(f"[bold blue]=== ターン {self.current_turn} ===[/bold blue]")

        if not self.players[player]:
            logging.warning(f"{player} に手札がありません。ターンをスキップします。")
            return

        # 手札から最初のカードを選んで場に出す
        card_to_play = self.players[player].pop(0)
        console.print(f"[bold]{player}[/bold] が {card_to_play} をプレイしました。")

        # 手札のカードで場の札と合札を試みる
        self.handle_card_play(player, card_to_play)

        # 山札からカードを引く
        if self.card_manager.cards:
            drawn_card = self.card_manager.draw_card()
            console.print(f"[bold]{player}[/bold] が山札から {drawn_card} を引きました。")

            # 山札のカードで場の札と合札を試みる
            self.handle_card_play(player, drawn_card)
        else:
            logging.warning("山札が空です。")

        # ターン終了後にゲーム状態を表示
        self.display_game_state()

    def handle_card_play(self, player, card):
        """
        指定したカードを場に出し、合札を試みる
        :param player: プレイヤー名
        :param card: 場に出すカード
        """
        # 場で同じ月のカードを探す
        matching_cards = [field_card for field_card in self.field if field_card.month == card.month]

        if matching_cards:
            # 合札処理
            matched_card = matching_cards[0]
            self.field.remove(matched_card)
            console.print(f"[bold]{player}[/bold] は {card} と {matched_card} を合札しました。")
            self.acquired[player][matched_card.category].extend([card, matched_card])
        else:
            # 合札できない場合は場に置く
            self.field.append(card)
            console.print(f"[bold]{player}[/bold] は場に {card} を置きました。")

    def check_scores(self):
        """
        各プレイヤーの得点を計算し、役ができた場合に「こいこい」または「あがり」を選択
        """
        for player in self.players:
            all_acquired_cards = sum(self.acquired[player].values(), [])
            roles = self.card_manager.check_roles(all_acquired_cards)
            points = self.card_manager.calculate_points(roles)

            if roles:  # 役がある場合
                console.print(f"[bold]{player}[/bold] の役: [yellow]{roles}[/yellow] (得点: {points})")
                choice = self.get_player_choice(player, roles, points)

                if choice == "あがり":
                    console.print(f"[bold]{player}[/bold] が「あがり」を選択しました！")
                    self.scores[player] += points
                    return "end_round"
                else:
                    console.print(f"[bold]{player}[/bold] が「こいこい」を選択しました。")
            else:
                console.print(f"[bold]{player}[/bold] の得点: {self.scores[player]} (役なし)")

        return "continue_round"

    def get_player_choice(self, player, roles, points):
        """
        プレイヤーが役を作った際に「こいこい」または「あがり」を選択
        :param player: プレイヤー名
        :param roles: 作成された役
        :param points: 獲得した得点
        :return: 選択結果 ("こいこい" or "あがり")
        """
        # 現在は自動的にランダム選択する（将来的にはAIやUIで制御可能）
        from random import choice
        return choice(["こいこい", "あがり"])

    def initialize_round(self):
        """
        ラウンドを初期化
        """
        self.card_manager.initialize_cards()  # カードを初期化
        self.card_manager.shuffle_deck()  # デッキをシャッフル
        logging.info("ラウンドを初期化しました。山札をシャッフルしました。")

        # 各プレイヤーと場にカードを配布
        for player in self.players:
            self.players[player] = [self.card_manager.draw_card() for _ in range(8)]
        self.field = [self.card_manager.draw_card() for _ in range(8)]
        self.display_game_state()

    def start_game(self, rounds=12):
        """
        ゲーム全体を管理
        """
        self.initialize_game()  # ゲーム開始時の初期化

        for round_number in range(1, rounds + 1):
            console.print(f"[bold magenta]=== ラウンド {round_number} ===[/bold magenta]")
            self.current_turn = 0  # ラウンド開始時にターン数をリセット

            round_status = "continue_round"
            while round_status == "continue_round":
                for player in self.players:
                    self.play_turn(player)
                    round_status = self.check_scores()
                    if round_status == "end_round":
                        break

            console.print(f"[bold red]ラウンド {round_number} 終了！[/bold red]")

            # 次のラウンドに向けて初期化
            if round_number < rounds:
                self.initialize_round()

        console.print("[bold green]=== ゲーム終了 ===[/bold green]")
        console.print("[bold green]最終スコア:[/bold green]", self.scores)