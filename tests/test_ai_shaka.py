import sys
import os

# プロジェクトルートを検索パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.ai.characters.ai_shaka import ShakaAI

def test_decide_action():
    ai = ShakaAI()
    state = {
        "available_actions": [
            {"category": "光", "month": 3},
            {"category": "短冊", "month": 1},
            {"category": "カス", "month": 5}
        ]
    }
    action = ai.decide_action(state)
    assert action in state["available_actions"]
    assert action["category"] in ["光", "短冊"]

def test_decide_koikoi():
    ai = ShakaAI()
    state = {
        "current_score": 5,
        "opponent_score": 7
    }
    assert ai.decide_koikoi(state) is True

    state = {
        "current_score": 8,
        "opponent_score": 5
    }
    assert ai.decide_koikoi(state) is False
