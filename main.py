from src.game.game_manager import GameManager
from src.ai.characters.ai_shaka import ShakaAI

# ShakaAIを使ったテストゲーム
def main():
    print("こいこいゲームの進行テストを開始します！")
    
    # プレイヤー（またはAI）の作成
    player1 = ShakaAI()
    player2 = ShakaAI()
    
    # ゲームマネージャーの作成
    game_manager = GameManager(player1, player2)
    
    # ゲームを開始
    game_manager.start_game()

if __name__ == "__main__":
    main()
