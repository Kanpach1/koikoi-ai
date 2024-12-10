class BaseAI:
    def __init__(self, name):
        self.name = name

    def decide_action(self, state):
        """
        ゲーム状態を基に行動を決定。
        :param state: ゲームの状態
        :return: 行動
        """
        raise NotImplementedError("This method should be overridden by subclasses")
