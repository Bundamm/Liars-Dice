"""
Game handler for the Liar's Dice game.

This module provides the GameHandler class, which manages the overall game flow,
player creation, turns, and game state.
"""

from src.players import Player
from src.round_handler import RoundHandler
from src.state import GameState, PlayerState
from src.bid import Bid


class GameHandler:
    """
    A class that manages the overall flow of the Liar's Dice game.

    The GameHandler is responsible for creating players, managing game rounds,
    handling player turns, and tracking the state of the game.
    """

    def __init__(self, players_names: list[str], dice_count: int) -> None:
        """
        Initialize a new game with the given player names and dice count.

        Args:
            players_names: List of player names
            dice_count: Number of dice each player starts with

        Raises:
            TypeError: If dice_count is not an integer
            ValueError: If dice_count is less than 1
        """
        if not isinstance(dice_count, int):
            raise TypeError("Dice count must be an integer")
        if dice_count < 1:
            raise ValueError("Dice count must be more or equal to 1")
        self.players_names = players_names
        self.dice_count = dice_count
        self.players = self.create_players(self.players_names)
        self.round_handler = RoundHandler(self.players)
        self.game_state = GameState.RUNNING

    def create_players(self, players_names: list[str]) -> list[Player]:
        """
        Create Player objects for each name in the list.

        Args:
            players_names: List of player names

        Returns:
            List of Player objects

        Raises:
            TypeError: If players_names contains non-string elements
        """
        if not all(isinstance(player_name, str) for player_name in players_names):
            raise TypeError("Players_names must be a list of strings")
        players = []
        for name in players_names:
            players.append(Player(name, self.dice_count))
        return players

    def play_bid_turn(
        self, active_player: Player, number_of_dice: int, dice_value: int
    ) -> None:
        """
        Execute a bid turn for the active player.

        Args:
            active_player: The player making the bid
            number_of_dice: Quantity of dice claimed in the bid
            dice_value: Value of dice claimed in the bid

        Raises:
            TypeError: If parameters are not of the correct types
            Exception: If the player is not active
        """
        if not isinstance(active_player, Player):
            raise TypeError("Active player must be a Player instance")
        if not isinstance(number_of_dice, int):
            raise TypeError("Number of dice must be an integer")
        if not isinstance(dice_value, int):
            raise TypeError("Dice value must be an integer")
        if active_player.state != PlayerState.ACTIVE:
            raise Exception("Player is not active")
        self.round_handler.make_bid(active_player.name, number_of_dice, dice_value)

    def play_challenge_turn(self, active_player: Player) -> str:
        """
        Execute a challenge turn for the active player.

        The active player challenges the previous bid, ending the current round.

        Args:
            active_player: The player making the challenge

        Returns:
            Name of the player who lost the challenge

        Raises:
            TypeError: If active_player is not a Player
            Exception: If the player is not active
        """
        if not isinstance(active_player, Player):
            raise TypeError("Active player must be a Player instance")
        if not active_player.state == PlayerState.ACTIVE:
            raise Exception("Player is not active")
        challenge = self.round_handler.challenge_and_end_round(active_player.name)
        return challenge

    @staticmethod
    def play_check_turn(active_player: Player) -> list[int]:
        """
        Return the dice values from the active player's last roll.

        This allows a player to check their own dice.

        Args:
            active_player: The player checking their dice

        Returns:
            List of dice values from the player's last roll

        Raises:
            TypeError: If active_player is not a Player
            Exception: If the player is not active
        """
        if not isinstance(active_player, Player):
            raise TypeError("Active player must be a Player instance")
        if not active_player.state == PlayerState.ACTIVE:
            raise Exception("Player is not active")
        return active_player.last_roll

    def get_active_player(self) -> Player:
        """
        Get the player whose turn it currently is.

        Returns:
            The active player

        Raises:
            Exception: If no player is active
        """
        return self.round_handler.get_active_player()

    def start_round(self) -> None:
        """
        Start a new round of the game.

        This rolls dice for all players and activates the first player.
        """
        self.round_handler.start_round()

    def get_round_number(self) -> int:
        """
        Get the current round number.

        Returns:
            The current round number
        """
        return self.round_handler.round_number

    def get_current_bid(self) -> Bid | None:
        """
        Get the current bid in play.

        Returns:
            The current bid, or None if no bid has been made yet
        """
        return self.round_handler.current_bid

    def check_if_start_next_round(self) -> bool:
        """
        Check if the game should continue to another round.

        Returns:
            True if there are at least two players still in the game
        """
        return self.round_handler.check_if_start_next_round()

    def end_game_info(self) -> str:
        """
        Get information about the game's end state.

        Returns:
            The name of the winner

        Raises:
            Exception: If there is no winner
        """
        return self.round_handler.end_game_info()
