import random
from app.pycardgame import UnoCard, UnoDeck, UnoGame, UnoPlayer


def move(game: UnoGame):
    for card in game.get_current_player():
        if game.check_valid_play(card, game.get_top_card()):
            print(f"{game.get_current_player().name} plays {card}")
            if card.get_suit() == "Wild":  # randomly change color
                new_suit = random.choice(UnoCard.SUITS)
                print(f"-> Changed color to {new_suit}")
            else:
                new_suit = None
            game.play_card(game.get_current_player(), card, new_suit)
            game.next_player()
            break
    else:
        drawn_card = game.draw_card(game.get_current_player())[0]
        print(f"{game.get_current_player().name} cannot play any card. "
              f"Drawing a card: {drawn_card!s}")
        game.next_player()
    # print(f"=> {game.get_current_player().name}'s turn.")


def main():
    random.seed(42)

    player1 = UnoPlayer("Alice")
    player2 = UnoPlayer("Bob")
    player3 = UnoPlayer("Charlie")
    player4 = UnoPlayer("Diana")

    deck = UnoDeck().shuffle()

    game = UnoGame(player1, player2, player3, player4, deck=deck)
    game.start_game()  # Start the game. Top card: Yellow 2
    print(game)

    for player in game.players:
        print(f"{player.name} has {len(player.hand)} cards:")
        for card in sorted(player):
            print(f" - {card}")

    print()
    move(game)  # Alice plays Green 2
    for player in game.players:
        print(f"{player.name} has {len(player.hand)} cards")
    print()

    move(game)  # Bob plays Green 5
    move(game)  # Charlie plays Green 1
    move(game)  # Diana plays Wild Draw Four and changes color to Red

    move(game)  # Alice plays Red Skip
    move(game)  # Charlie plays Red 0
    move(game)  # Diana draws Wild

    move(game)  # Alice plays Red 7
    move(game)  # Bob plays Green 7
    move(game)  # Charlie plays Wild and changes color to Red
    print(f"-> Changed color to {game.get_top_card().get_suit()}")
    move(game)

    for player in game.players:
        print(f"{player.name} has {len(player.hand)} cards")


if __name__ == "__main__":
    main()
