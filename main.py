# main.py

from cards.deck import Deck
from game.game import Game

def main():
    # デッキを準備してシャッフル
    deck = Deck()
    deck.shuffle()
    deck.deal()

    # ゲームを開始
    game = Game(deck)
    game.play()

if __name__ == "__main__":
    main()
