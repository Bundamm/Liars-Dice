"""
Die implementation for the Liar's Dice game.
This module provides the Die class, which simulates a die with a customizable
number of sides (default is 6).
"""

from random import randint


class Die:
    """
    A class representing a single die with a configurable number of sides.
    The Die class simulates a die that can be rolled to produce random values
    between 1 and the number of sides.
    """

    def __init__(self, sides: int = 6) -> None:
        """
        Initialize a new Die with the specified number of sides.

        Args:
            sides: Number of sides on the die (default: 6)

        Raises:
            ValueError: If sides is less than or equal to 1
            TypeError: If sides is not an integer
        """
        if sides <= 1:
            raise ValueError("Number of sides must be greater than 1")
        if not isinstance(sides, int):
            raise TypeError("Number of sides must be an integer")
        self.sides = sides

    def roll(self) -> int:
        """
        Roll the die and return a random value between 1 and the number of sides.

        Returns:
            A random integer between 1 and the number of sides
        """
        return randint(1, self.sides)

    def roll_dice(self, num: int) -> list[int]:
        """
        Roll the die multiple times and return a list of results.

        Args:
            num: Number of times to roll the die

        Returns:
            A list of random integers between 1 and the number of sides

        Raises:
            TypeError: If num is not an integer
            ValueError: If num is less than or equal to 0
        """
        if not isinstance(num, int):
            raise TypeError("Number of times thrown must be an integer")
        if num <= 0:
            raise ValueError("Number of times thrown must be greater than 0")
        rolls = []
        for _ in range(num):
            rolls.append(self.roll())
        return rolls

    def set_sides(self, sides: int) -> None:
        """
        Change the number of sides on the die.

        Args:
            sides: New number of sides for the die

        Raises:
            TypeError: If sides is not an integer
            ValueError: If sides is less than or equal to 1
        """
        if not isinstance(sides, int):
            raise TypeError("Number of sides must be an integer")
        if sides <= 1:
            raise ValueError("Number of sides must be greater than 1")
        self.sides = sides

    def __str__(self) -> str:
        """
        Return a string representation of the die.

        Returns:
            A string in the format "Die(X sides)" where X is the number of sides
        """
        return f"Die({self.sides} sides)"
