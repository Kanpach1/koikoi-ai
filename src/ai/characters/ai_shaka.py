from src.ai.base_ai import BaseAI

class ShakaAI(BaseAI):
    """
    正（ShakaAI）: ルールベースのバランス型AI
    """
    def __init__(self):
        super().__init__("シャカ")

    def decide_action(self, state):
        """
        バランスを重視した行動を決定
        :param state: 現在のゲーム状態
        :return: プレイするカード
        """
        available_actions = state["available_actions"]
        if not available_actions:
            return None  # 行動がない場合はパス

        # 1. 役に関与するカードを優先
        prioritized_actions = self.prioritize_actions(state, available_actions)
        if prioritized_actions:
            return prioritized_actions[0]

        # 2. 次に点数が取れそうなカードを選択
        scored_actions = self.evaluate_actions(state, available_actions)
        return max(scored_actions, key=scored_actions.get)

    def prioritize_actions(self, state, actions):
        """
        役の成立に重要なカードを優先
        :param state: 現在のゲーム状態
        :param actions: 利用可能な行動のリスト
        :return: 優先行動のリスト
        """
        priority_actions = []
        for action in actions:
            # 例: 光を優先
            if action["category"] == "光":
                priority_actions.append(action)
            elif action["category"] == "短冊" and action["month"] in [1, 2, 3]:
                priority_actions.append(action)  # 赤短を優先
        return priority_actions

    def evaluate_actions(self, state, actions):
        """
        各行動を評価してスコアを付与
        :param state: 現在のゲーム状態
        :param actions: 行動のリスト
        :return: スコア付きの行動
        """
        action_scores = {}
        for action in actions:
            # ダミー例: カテゴリごとにスコアを設定
            if action["category"] == "光":
                action_scores[action] = 10
            elif action["category"] == "タネ":
                action_scores[action] = 5
            elif action["category"] == "短冊":
                action_scores[action] = 7
            else:
                action_scores[action] = 1
        return action_scores

    def decide_koikoi(self, state):
        """
        こいこいするかどうかを決定
        :param state: 現在のゲーム状態
        :return: True（こいこい）または False（終了）
        """
        current_score = state["current_score"]
        opponent_score = state["opponent_score"]
        if current_score < opponent_score:
            return True  # 点差がある場合はリスクを取る
        elif current_score >= 7:
            return False  # 安全策で終了
        else:
            return True  # デフォルトでこいこい
