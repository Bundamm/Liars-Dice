"""
Player implementation for the Liar's Dice game.

This module provides the Player class, which represents a player in the game,
maintaining the player's dice, state, and game actions.
"""

from src.dice import Die
from src.state import PlayerState


class Player:
    """
    A class representing a player in the Liar's Dice game.

    Each player has a name, a collection of dice, a state (active, waiting, etc.),
    and a record of their last dice roll.
    """

    def __init__(self, name: str, dice_count: int) -> None:
        """
        Initialize a new Player with a name and a number of dice.

        Args:
            name: The player's name
            dice_count: The number of dice the player starts with

        Raises:
            TypeError: If name is not a string or dice_count is not an integer
            ValueError: If dice_count is less than 1
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(dice_count, int):
            raise TypeError("Dice count must be an integer")
        if dice_count < 1:
            raise ValueError("Dice count must be greater than 0")
        self.name = name
        self.state = PlayerState.WAITING
        self.dice = [Die() for _ in range(dice_count)]
        self.last_roll: list[int] = []

    def make_roll(self, count: int) -> list[int]:
        """
        Roll the specified number of dice and record the results.

        Args:
            count: Number of dice to roll

        Returns:
            List of dice values from the roll

        Raises:
            ValueError: If count is less than 1 or greater than the player's dice count
        """
        if count < 1:
            raise ValueError("Number of dice to roll must be greater than 0")
        if count > len(self.dice):
            raise ValueError(
                "Number of dice to roll must be less or equal to the number of dice in game"
            )
        copy_roll = self.last_roll.copy()
        for i in range(count):
            copy_roll.append(self.dice[i].roll())
        self.last_roll = copy_roll
        return copy_roll

    def lose_die(self) -> None:
        """
        Remove one die from the player's collection.

        If the player loses their last die, their state is set to LOST.
        """
        self.dice.pop()
        if len(self.dice) == 0:
            self.state = PlayerState.LOST

    def get_dice_count(self) -> int:
        """
        Get the number of dice the player currently has.

        Returns:
            The number of dice
        """
        return len(self.dice)

    def get_die_value(self) -> int:
        """
        Get the number of sides on the player's dice.

        Returns:
            The number of sides on the dice
        """
        number = self.dice[0].sides
        return number

    def is_active(self) -> bool:
        """
        Check if the player is currently active (taking their turn).

        Returns:
            True if the player's state is ACTIVE, False otherwise
        """
        return self.state == PlayerState.ACTIVE

    def reset_roll(self) -> None:
        """
        Clear the player's last roll record.

        Raises:
            Exception: If the player has lost (has no dice)
        """
        if self.state == PlayerState.LOST:
            raise Exception("Player cannot roll dice after losing")
        self.last_roll.clear()

    def __str__(self) -> str:
        """
        Return a string representation of the player.

        Returns:
            A string in the format "Player(name, X dice)" where X is the dice count
        """
        return f"Player({self.name}, {self.get_dice_count()} dice)"

    def set_state(self, state: PlayerState) -> None:
        """
        Set the player's state to a new value.

        Args:
            state: The new state to set

        Raises:
            TypeError: If state is not a PlayerState
            Exception: If the player has already lost (can't change state)
        """
        if not isinstance(state, PlayerState):
            raise TypeError(f"Expected PlayerState but got {format(type(state))}")
        if self.state == PlayerState.LOST:
            raise Exception("Player cannot come back after losing")
        self.state = state
