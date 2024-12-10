import pytest
from src.cards.card_manager import Card


def test_card_equality():
    """
    Card クラスの __eq__ メソッドのテスト
    """
    # 同じ月とカテゴリの場合
    card1 = Card(3, "光")
    card2 = Card(3, "光")
    assert card1 == card2  # 等価

    # 異なる月の場合
    card3 = Card(4, "光")
    assert card1 != card3  # 非等価

    # 異なるカテゴリの場合
    card4 = Card(3, "短冊")
    assert card1 != card4  # 非等価

    # 他の型との比較
    assert card1 != "Not a Card"  # 非等価
    assert card1 != None  # 非等価
