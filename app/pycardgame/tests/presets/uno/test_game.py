from .... import NumberCard, UnoPlayer


def test_uno_player_init():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    assert player.name == "Player 1"
    assert len(player) == 1
    assert isinstance(player.hand[0], NumberCard)


def test_uno_player_call_uno():
    player = UnoPlayer("Player 1")
    player.call_uno()
    assert player.uno is False

    player.hand = [NumberCard("5", "Red")]
    player.call_uno()
    assert player.uno is True


def test_uno_player_reset_uno():
    player = UnoPlayer("Player 1", None, True)
    player.reset_uno()
    assert player.uno is False


def test_uno_player_str():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    assert str(player) == "Player Player 1 (1 card(s)):\n - Red 5"


def test_uno_player_repr():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    assert repr(player) == ("UnoPlayer('Player 1', "
                            "hand=[NumberCard(rank=5, suit=0)], uno=False)")
