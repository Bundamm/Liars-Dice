"""
Round handler for the Liar's Dice game.

This module provides the RoundHandler class, which manages the flow of a single round,
including bid validation, player turns, challenge resolution, and penalties.
"""

from src.players import Player
from src.state import PlayerState
from src.bid import Bid
from typing import List, Optional


class RoundHandler:
    """
    A class that manages the flow of a single round in the Liar's Dice game.

    The RoundHandler tracks the current state of the round, including the current player,
    the current bid, and handles the logic for bidding, challenging, and resolving a round.
    """

    def __init__(self, players: List[Player]) -> None:
        """
        Initialize a new round handler with a list of players.

        Args:
            players: List of players participating in the game

        Raises:
            TypeError: If players is not a list of Player objects
        """
        if not all(isinstance(player, Player) for player in players):
            raise TypeError("Players must be a list of Player objects")
        self.players = players
        self.round_number = 0
        self.current_player_id = 0
        self.current_bid: Optional[Bid] = None
        self.dice_count = sum(player.get_dice_count() for player in players)

    def start_round(self) -> None:
        """
        Start a new round.

        Increments the round number, makes all players roll their dice,
        and sets the first player to active.
        """
        self.round_number += 1
        for player in self.players:
            player.make_roll(player.get_dice_count())
        self.current_bid = None
        self.players[self.current_player_id].set_state(PlayerState.ACTIVE)

    def make_bid(self, player_name: str, number_of_dice: int, dice_value: int) -> None:
        """
        Process a bid made by a player.

        Validates the bid parameters, creates a new Bid object, checks if it's higher
        than the previous bid, and advances to the next player.

        Args:
            player_name: Name of the player making the bid
            number_of_dice: Quantity of dice claimed in the bid
            dice_value: Value of dice claimed in the bid

        Raises:
            TypeError: If parameters are not of the correct types
            ValueError: If the bid parameters are invalid or the player is not active
        """
        if not isinstance(player_name, str):
            raise TypeError(
                f"Player name must be str but got {format(type(player_name))}"
            )
        player = self.get_player_by_name(player_name)
        if not isinstance(dice_value, int):
            raise TypeError(
                f"Dice value must be an integer but got {format(type(dice_value))}"
            )
        if not isinstance(number_of_dice, int):
            raise TypeError(
                f"Number of dice must be an integer but got \
                {format(type(number_of_dice))}"
            )
        if dice_value < 1:
            raise ValueError("Bid value must be greater than 0")
        if dice_value > player.get_die_value():
            raise ValueError(
                "Bid value must be less or equal to the value of dice in game"
            )
        if number_of_dice > self.dice_count:
            raise ValueError(
                "Number of dice must be equal or less than number of dice in game"
            )
        if player.state != PlayerState.ACTIVE:
            raise ValueError(f"Player {player_name} is not active")
        previous_bid = self.current_bid
        new_bid = Bid(number_of_dice, dice_value, player)
        if not self.is_higher_bid(new_bid, previous_bid):
            raise ValueError("Bid must be higher than the previous one!")
        self.current_bid = new_bid
        self.next_player()

    @staticmethod
    def is_higher_bid(new_bid: Bid, current_bid: Optional[Bid]) -> bool:
        """
        Check if a new bid is higher than the current bid.

        A bid is higher if it has a higher quantity, or the same quantity but a higher value.
        The first bid (when current_bid is None) is always considered higher.

        Args:
            new_bid: The new bid to check
            current_bid: The current bid to compare against, or None if this is the first bid

        Returns:
            True if the new bid is higher, False otherwise
        """
        if current_bid is None:
            return True
        if new_bid.quantity > current_bid.quantity:
            return True
        if (
            new_bid.quantity == current_bid.quantity and
            new_bid.value > current_bid.value
        ):
            return True
        return False

    def next_player(self) -> None:
        """
        Advance to the next player in the rotation.

        Sets the current player to waiting, then finds the next player in the rotation
        who is in the waiting state and makes them active.
        """
        self.players[self.current_player_id].state = PlayerState.WAITING
        while True:
            self.current_player_id = (self.current_player_id + 1) % len(self.players)
            next_player = self.players[self.current_player_id]
            if next_player.state == PlayerState.WAITING:
                break
        self.players[self.current_player_id].state = PlayerState.ACTIVE

    def challenge_and_end_round(self, player_name: str) -> str:
        """
        Process a challenge made by a player and end the current round.

        Counts the dice with the bid value, determines the loser of the challenge,
        applies penalties, and prepares for the next round.

        Args:
            player_name: Name of the player making the challenge

        Returns:
            Name of the player who lost the challenge

        Raises:
            TypeError: If player_name is not a string
            ValueError: If there is no bid to challenge or the player is not active
        """
        if not isinstance(player_name, str):
            raise TypeError("Player name must be a string")
        if self.current_bid is None or not self.current_bid.player:
            raise ValueError("No bid to challenge")
        player = self.get_player_by_name(player_name)
        if player.state != PlayerState.ACTIVE:
            raise ValueError(f"Player {player_name} is not active")

        bidder = self.current_bid.player
        challenger = player
        target_value = self.current_bid.value
        target_dice_amount = self.current_bid.quantity

        value_of_die = self.count_dice_value(target_value)
        loser = self.resolve_challenge(
            bidder, challenger, target_dice_amount, value_of_die
        )
        self.apply_penalty(loser)
        self.reset_players_after_round()

        if self.check_if_start_next_round():
            self.start_round()
        else:
            self.end_game_info()
        return loser.name

    def count_dice_value(self, value: int) -> int:
        """
        Count how many dice with the specified value are in play.

        Args:
            value: The face value to count

        Returns:
            The number of dice with the specified value

        Raises:
            ValueError: If value is not valid
        """
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")
        max_die_value = self.players[self.current_player_id].get_die_value()
        if value < 1 or value > max_die_value:
            raise ValueError(f"Value must be between 1 and {max_die_value}")
        count = 0
        for player in self.players:
            for roll in player.last_roll:
                if roll == value:
                    count += 1
        return count

    def apply_penalty(self, player: Player) -> None:
        """
        Apply a penalty to a player who lost a challenge.

        Removes one die from the player and eliminates them if they have no dice left.

        Args:
            player: The player to penalize

        Raises:
            Exception: If player is not a Player instance
        """
        if not isinstance(player, Player):
            raise Exception("Player must be an instance of Player")
        player.lose_die()
        if player.get_dice_count() == 0:
            self.eliminate_player(player)

    def reset_players_after_round(self) -> None:
        """
        Reset all players for the next round.

        Clears all players' roll records, eliminates players with no dice,
        and sets remaining players to waiting.
        """
        for player in self.players:
            player.reset_roll()
            if player.get_dice_count() == 0:
                self.eliminate_player(player)
            else:
                player.set_state(PlayerState.WAITING)

    def get_player_by_name(self, name: str) -> Player:
        """
        Find a player by their name.

        Args:
            name: The name of the player to find

        Returns:
            The player with the specified name

        Raises:
            TypeError: If name is not a string
            Exception: If no player with the given name is found
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        for player in self.players:
            if player.name == name:
                return player
        raise Exception("Player not found")

    @staticmethod
    def eliminate_player(player: Player) -> None:
        """
        Eliminate a player from the game.

        Sets the player's state to LOST.

        Args:
            player: The player to eliminate

        Raises:
            Exception: If player is not a Player instance
        """
        if not isinstance(player, Player):
            raise Exception("Player must be an instance of Player")
        player.state = PlayerState.LOST

    @staticmethod
    def resolve_challenge(
        bidder: Player, challenger: Player, target_dice_amount: int, value_of_die: int
    ) -> Player:
        """
        Determine who loses a challenge.

        Args:
            bidder: The player who made the bid
            challenger: The player who challenged the bid
            target_dice_amount: The quantity from the bid
            value_of_die: The actual count of dice with the specified value

        Returns:
            The player who lost the challenge

        Raises:
            Exception: If parameters are not of the correct types
        """
        if not isinstance(challenger, Player):
            raise Exception("Challenger must be a Player")
        if not isinstance(bidder, Player):
            raise Exception("Bidder must be a Player")
        if not isinstance(target_dice_amount, int):
            raise TypeError("Target dice amount must be an integer")
        if not isinstance(value_of_die, int):
            raise TypeError("Value of die must be an integer")
        if value_of_die < target_dice_amount:
            return bidder
        return challenger

    def get_active_player(self) -> Player:
        """
        Get the player whose turn it currently is.

        Returns:
            The active player

        Raises:
            Exception: If no player is active
        """
        for player in self.players:
            if player.is_active():
                return player
        raise Exception("No active player")

    def check_if_start_next_round(self) -> bool:
        """
        Check if the game should continue to another round.

        Returns:
            True if there are at least two players still in the game
        """
        active_players = [
            player for player in self.players if player.state != PlayerState.LOST
        ]
        return len(active_players) > 1

    def end_game_info(self) -> str:
        """
        Get information about the game's end state.

        Returns:
            The name of the winner

        Raises:
            Exception: If there is no winner
        """
        winners = [p for p in self.players if p.state != PlayerState.LOST]
        if winners:
            winner = winners[0]
            return winner.name
        raise Exception("No winner")
