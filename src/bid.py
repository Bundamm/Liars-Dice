"""
Bid implementation for the Liar's Dice game.

This module provides the Bid class, which represents a player's claim about
how many dice of a particular value are present in the game.
"""

from src.players import Player


class Bid:
    """
    A class representing a bid made by a player during the Liar's Dice game.

    A bid consists of a quantity (how many dice), a value (the face value of the dice),
    and the player who made the bid.
    """

    def __init__(self, quantity: int, value: int, player: Player) -> None:
        """
        Initialize a new Bid.

        Args:
            quantity: Number of dice claimed
            value: Face value of the dice claimed
            player: Player making the bid

        Raises:
            ValueError: If quantity or value is less than 1
            TypeError: If player is not a Player instance
            ValueError: If player is not active
        """
        if not isinstance(quantity, int) or not isinstance(value, int):
            raise ValueError("Quantity and value must be integers")
        if player is None or not isinstance(player, Player):
            raise TypeError("Player must be a Player instance")
        if quantity < 1 or value < 1:
            raise ValueError("Quantity and value must be greater than 0")
        if not player.is_active():
            raise ValueError("Player is not active")
        self.quantity = quantity
        self.value = value
        self.player = player

    def __str__(self) -> str:
        """
        Return a string representation of the bid.

        Returns:
            A string in the format "Bid(quantity, value, player_name)"
        """
        return f"Bid({self.quantity}, {self.value}, {self.player.name})"

    def __eq__(self, other: object) -> bool:
        """
        Check if this bid is equal to another bid.

        Args:
            other: Another object to compare with

        Returns:
            True if the bids have the same quantity, value, and player name
        """
        return (
            isinstance(other, Bid) and
            self.quantity == other.quantity and
            self.value == other.value and
            self.player.name == other.player.name
        )

    def __gt__(self, other: object) -> bool:
        """
        Check if this bid is greater than another bid.

        A bid is greater if it claims a higher quantity of dice,
        or the same quantity but a higher face value.

        Args:
            other: Another object to compare with

        Returns:
            True if this bid is higher than the other bid
        """
        if not isinstance(other, Bid):
            raise TypeError("Other must be a Bid instance")
        return (
            self.quantity > other.quantity or
            self.value > other.value
        )

    def __lt__(self, other: object) -> bool:
        """
        Check if this bid is less than another bid.

        A bid is less if it claims a lower quantity of dice,
        or the same quantity but a lower face value.

        Args:
            other: Another object to compare with

        Returns:
            True if this bid is lower than the other bid
        """
        if not isinstance(other, Bid):
            raise TypeError("Other must be a Bid instance")
        return (
            self.quantity < other.quantity or
            self.value < other.value
        )

    def get_player_name(self) -> str:
        """
        Get the name of the player who made this bid.

        Returns:
            The name of the player
        """
        return self.player.name
