import pytest
from src.cards.card_manager import Card, CardManager


def test_card_initialization():
    """
    Card クラスの初期化と文字列表現のテスト
    """
    card = Card(1, "光")
    assert card.month == 1
    assert card.category == "光"
    assert card.is_kasu_point is False
    assert repr(card) == "1月の光"

    card_with_kasu = Card(9, "カス", is_kasu_point=True)
    assert card_with_kasu.is_kasu_point is True
    assert repr(card_with_kasu) == "9月のカス（カス得点）"


def test_card_manager_initialization():
    """
    CardManager の初期化とカード生成テスト
    """
    manager = CardManager()
    manager.initialize_cards()
    assert len(manager.cards) == 48
    assert isinstance(manager.cards[0], Card)


def test_role_detection():
    """
    役判定ロジックのテスト
    """
    manager = CardManager()

    # 五光の役
    cards_five_light = [
        Card(1, "光"), Card(3, "光"), Card(8, "光"),
        Card(11, "光"), Card(12, "光")
    ]
    roles = manager.check_roles(cards_five_light)
    assert "五光" in roles

    # 赤短の役
    cards_red_short = [
        Card(1, "短冊"), Card(2, "短冊"), Card(3, "短冊")
    ]
    roles = manager.check_roles(cards_red_short)
    assert "赤短" in roles

    # 青短の役
    cards_blue_short = [
        Card(6, "短冊"), Card(9, "短冊"), Card(10, "短冊")
    ]
    roles = manager.check_roles(cards_blue_short)
    assert "青短" in roles

    # 赤短と青短の重複
    cards_red_and_blue = [
        Card(1, "短冊"), Card(2, "短冊"), Card(3, "短冊"),
        Card(6, "短冊"), Card(9, "短冊"), Card(10, "短冊")
    ]
    roles = manager.check_roles(cards_red_and_blue)
    assert "赤短" not in roles
    assert "青短" not in roles
    assert "赤短・青短の重複" in roles

    # 短冊5枚の役
    cards_many_short = [
        Card(1, "短冊"), Card(2, "短冊"), Card(3, "短冊"),
        Card(4, "短冊"), Card(5, "短冊")
    ]
    roles = manager.check_roles(cards_many_short)
    assert "短冊（5枚）" in roles


def test_point_calculation():
    """
    点数計算ロジックのテスト
    """
    manager = CardManager()

    roles = ["五光", "猪鹿蝶", "赤短"]
    points = manager.calculate_points(roles)
    assert points == 20  # 10（五光）+ 5（猪鹿蝶）+ 5（赤短）

    roles = ["赤短・青短の重複", "短冊（7枚）"]
    points = manager.calculate_points(roles)
    assert points == 13  # 10（重複）+ 3（短冊追加点: 1+2）

    roles = ["タネ（6枚）", "カス（12枚）"]
    points = manager.calculate_points(roles)
    assert points == 5  # 1+1（タネ）+ 1+2（カス）


def test_invalid_input():
    """
    無効な入力に対するエラーチェック
    """
    manager = CardManager()
    with pytest.raises(ValueError):
        manager.check_roles("invalid input")
    with pytest.raises(ValueError):
        manager.check_roles([Card(1, "光"), "not a card"])

def test_check_roles_special_cases():
    manager = CardManager()

    # 猪鹿蝶が成立するケース
    cards_inoshikacho = [
        Card(7, "タネ"),  # 猪
        Card(10, "タネ"),  # 鹿
        Card(6, "タネ"),  # 蝶
    ]
    roles = manager.check_roles(cards_inoshikacho)
    assert "猪鹿蝶" in roles

    # 短冊のエッジケース（4枚では役なし）
    cards_no_short = [
        Card(1, "短冊"), Card(2, "短冊"), Card(3, "短冊"),
        Card(4, "短冊")
    ]
    roles = manager.check_roles(cards_no_short)
    assert "短冊（4枚）" not in roles

    # カスのエッジケース（9枚では役なし）
    cards_no_kasu = [
        Card(1, "カス"), Card(2, "カス"), Card(3, "カス"),
        Card(4, "カス"), Card(5, "カス"), Card(6, "カス"),
        Card(7, "カス"), Card(8, "カス"), Card(9, "カス")
    ]
    roles = manager.check_roles(cards_no_kasu)
    assert "カス（9枚）" not in roles

def test_calculate_points_edge_cases():
    manager = CardManager()

    # 短冊5枚の最低得点
    roles = ["短冊（5枚）"]
    points = manager.calculate_points(roles)
    assert points == 1  # 最低1点

    # タネ7枚の得点（1点 + ボーナス2点）
    roles = ["タネ（7枚）"]
    points = manager.calculate_points(roles)
    assert points == 3  # 1 + 2（ボーナス）

    # カス11枚の得点（1点 + ボーナス1点）
    roles = ["カス（11枚）"]
    points = manager.calculate_points(roles)
    assert points == 2  # 1 + 1（ボーナス）

def test_check_roles_invalid_input():
    manager = CardManager()

    with pytest.raises(ValueError):
        manager.check_roles("not a list")
    with pytest.raises(ValueError):
        manager.check_roles([Card(1, "光"), "invalid card"])

def test_check_roles_no_roles():
    manager = CardManager()

    # 役が成立しないケース
    cards_no_roles = [
        Card(1, "カス"), Card(2, "カス"), Card(3, "カス"),
        Card(4, "カス"), Card(5, "カス")
    ]
    roles = manager.check_roles(cards_no_roles)
    assert roles == []  # 役なし

def test_calculate_points_special_cases():
    manager = CardManager()

    # 特殊な役がない場合
    points = manager.calculate_points([])
    assert points == 0  # 得点なし

    # 不正な役が含まれている場合（追加チェック）
    points = manager.calculate_points(["不正な役"])
    assert points == 0  # 不正な役は無視される

def test_card_manager_empty_initialization():
    """
    CardManager の初期状態テスト（カード未初期化）
    """
    manager = CardManager()
    assert manager.cards == []  # 初期状態でカードリストは空

def test_check_roles_no_roles_special_cases():
    """
    特殊なケースで役が成立しない場合
    """
    manager = CardManager()

    # カードが空の場合
    roles = manager.check_roles([])
    assert roles == []  # 役なし

    # 光や短冊が単独で少ない場合
    cards_few_roles = [Card(1, "光"), Card(2, "短冊")]
    roles = manager.check_roles(cards_few_roles)
    assert roles == []  # 役なし

def test_calculate_points_empty_roles():
    """
    得点計算の特殊ケース（役なしの場合）
    """
    manager = CardManager()

    # 空の役リスト
    roles = []
    points = manager.calculate_points(roles)
    assert points == 0  # 得点なし
    
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