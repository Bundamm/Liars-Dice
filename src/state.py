"""
State definitions for the Liar's Dice game.

This module contains enumerations for player and game states used throughout the game.
"""

from enum import Enum


class PlayerState(Enum):
    """
    Enumeration of possible player states during the game.

    Attributes:
        ACTIVE: Player is currently taking their turn
        LOST: Player has lost all their dice and is out of the game
        WAITING: Player is waiting for their turn
        WON: Player has won the game
    """

    ACTIVE = 1
    LOST = 2
    WAITING = 3
    WON = 4


class GameState(Enum):
    """
    Enumeration of possible game states.

    Attributes:
        RUNNING: Game is in progress
        OVER: Game has ended
    """

    RUNNING = 1
    OVER = 2
