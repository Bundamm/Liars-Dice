"""
Liar's Dice game main file.
"""

from typing import Tuple, Optional
from src.game_handler import GameHandler
from src.state import GameState, PlayerState
from src.players import Player


def ask_action(current_player: Player, curr_game: GameHandler) -> str:
    """
    Display the current game state and prompt the player for their next action.
    Presents the current round number, shows the current bid if one exists,
    and asks the active player to choose an action (Bid, Challenge, or Check).
    Args:
        current_player (Player): The player whose turn it is
        curr_game (GameHandler): The current game instance
    Returns:
        str: The player's selected action ('Bid', 'Challenge', or 'Check')
    """
    print(f"\nROUND {curr_game.get_round_number()}")
    if curr_game.get_current_bid() is not None:
        print(f"Current bid: {curr_game.get_current_bid()}")
    else:
        print("No bid has been placed.")
    return input(f"{current_player.name}'s turn. (Bid/Challenge/Check): \n")


def clear_screen() -> None:
    """
    Clear the console screen by printing multiple newlines.
    This provides a simple way to separate turns visually
    and prevent players from seeing each other's dice.
    """
    print("\n" * 100)


def ask_bid() -> Tuple[int, int]:
    """
    Prompt the player for the details of their bid.
    Asks the player for the quantity and value of dice they want to bid.
    Returns:
        tuple: A pair of integers (number_of_dice, value_of_dice)
    Raises:
        ValueError: If the player enters non-integer values (handled by int conversion)
    """
    number_of_dice_to_bid = int(input("How many dice do you want to bid? "))
    value_of_dice_to_bid = int(input("What is the value of the dice? "))
    return number_of_dice_to_bid, value_of_dice_to_bid


def main() -> None:
    """
    Main function that runs the Liar's Dice game.
    Initializes the game, handles the main game loop, processes player actions,
    and determines the winner when the game ends.
    """
    # Initialize game with two players, each having 3 dice
    game = GameHandler(["Player1", "Player2"], 3)
    game.start_round()

    last_player_name: Optional[str] = None
    while game.game_state == GameState.RUNNING:
        # Get the active player for this turn
        active_player = game.get_active_player()
        if active_player is None:
            print("No active player")
            continue
        # Clear screen when it's a different player's turn
        if last_player_name != active_player.name:
            clear_screen()
            last_player_name = active_player.name
        try:
            # Process the player's chosen action
            action = ask_action(active_player, game)
            if action == "Bid":
                number_of_dice, dice_value = ask_bid()
                game.play_bid_turn(active_player, number_of_dice, dice_value)
            elif action == "Challenge":
                loser = game.play_challenge_turn(active_player)
                print(f"{loser} lost a die")
            elif action == "Check":
                result = game.play_check_turn(active_player)
                print(f"Your dice: {result}")
        except ValueError as e:
            print(e)
        # Check if the game should continue or end
        if not game.check_if_start_next_round():
            winner_name = game.end_game_info()
            if winner_name:
                for p in game.players:
                    if p.name == winner_name:
                        p.state = PlayerState.WON
                print(f"\nGame over! Winner is: {winner_name}")
            else:
                print("\nGame over! No winner (all players lost)")
            game.game_state = GameState.OVER


if __name__ == "__main__":
    main()
