"""
Tests that check the correctness of the Player class.

For example tests that check the correctness of the __init__ method,
the __str__ method, the roll method, and exceptions raised by the class.
"""

import unittest
from unittest.mock import patch
from src.players import Player
from src.state import PlayerState
from src.dice import Die


class TestPlayer(unittest.TestCase):
    """
    Test suite for the Player class that verifies player creation, state management,
    dice rolling and loss tracking. Tests include initialization, state transitions,
    and dice operations.
    """
    def setUp(self):
        """Set up test fixtures, creating players with different dice counts."""
        self.player = Player("Jan", 5)
        self.player2 = Player("Kowalski", 3)
        self.player3 = Player("Tomasz", 1)

    def test_init_valid(self):
        """Test that players are initialized correctly with valid inputs."""
        self.assertEqual(self.player.name, "Jan")
        self.assertEqual(self.player.get_dice_count(), 5)
        self.assertEqual(self.player.state, PlayerState.WAITING)

        self.assertEqual(self.player2.name, "Kowalski")
        self.assertEqual(self.player2.get_dice_count(), 3)
        self.assertEqual(self.player2.state, PlayerState.WAITING)

        self.assertEqual(self.player3.name, "Tomasz")
        self.assertEqual(self.player3.get_dice_count(), 1)
        self.assertEqual(self.player3.state, PlayerState.WAITING)

    def test_init_invalid_type_name(self):
        """Test that initialization fails with non-string player name."""
        with self.assertRaises(TypeError):
            Player(10, 5)

    def test_init_invalid_type_dice_count(self):
        """Test that initialization fails with non-numeric dice count."""
        with self.assertRaises(TypeError):
            Player("Jan", "5")

    def test_init_invalid_values(self):
        """Test that initialization fails with zero or negative dice count."""
        with self.assertRaises(ValueError):
            Player("Jan", 0)
        with self.assertRaises(ValueError):
            Player("Jan", -1)

    def test_roll_dice(self):
        """Test rolling dice with a mocked dice result."""
        with patch.object(Die, "roll", return_value=4):
            result = self.player.make_roll(3)
            self.assertEqual(result, [4, 4, 4])
            self.assertEqual(self.player.last_roll, [4, 4, 4])
            self.assertEqual(self.player.get_dice_count(), 5)

    def test_make_roll_invalid_count(self):
        """Test that rolling zero or negative dice raises a ValueError."""
        with self.assertRaises(ValueError):
            self.player.make_roll(0)
        with self.assertRaises(ValueError):
            self.player.make_roll(-1)

    def test_make_roll_with_too_many_dice(self):
        """Test that rolling more dice than the player has raises a ValueError."""
        with self.assertRaises(ValueError):
            self.player.make_roll(6)

    def test_make_roll_invalid_type(self):
        """Test that rolling a non-numeric count of dice raises a TypeError."""
        with self.assertRaises(TypeError):
            self.player.make_roll("5")

    def test_lose_die(self):
        """Test that a player loses one die when lose_die is called."""
        self.player.lose_die()
        self.assertEqual(self.player.get_dice_count(), 4)

    def test_lose_die_last_die(self):
        """Test that a player's state changes to LOST when they lose their last die."""
        for _ in range(self.player.get_dice_count()):
            self.player.lose_die()
        self.assertEqual(self.player.get_dice_count(), 0)
        self.assertEqual(self.player.state, PlayerState.LOST)

    def test_get_dice_count(self):
        """Test that get_dice_count returns the correct number of dice."""
        self.assertEqual(self.player.get_dice_count(), 5)
        self.player.lose_die()
        self.assertEqual(self.player.get_dice_count(), 4)

    def test_is_active(self):
        """Test that is_active returns the correct active status for different player states."""
        self.assertFalse(self.player.is_active())
        self.player.state = PlayerState.ACTIVE
        self.assertTrue(self.player.is_active())
        self.player.state = PlayerState.LOST
        self.assertFalse(self.player.is_active())
        self.player.state = PlayerState.WAITING
        self.assertFalse(self.player.is_active())

    def test_str(self):
        """Test the string representation of a player."""
        self.assertEqual(str(self.player), "Player(Jan, 5 dice)")

    def test_get_last_roll(self):
        """Test that the last roll is correctly stored and retrieved."""
        with patch.object(Die, "roll", return_value=3):
            result = self.player.make_roll(3)
            self.assertEqual(result, [3, 3, 3])
            self.assertEqual(self.player.last_roll, [3, 3, 3])

    def test_set_state_valid(self):
        """Test that a player's state can be changed to a valid state."""
        self.player.set_state(PlayerState.ACTIVE)
        self.assertEqual(self.player.state, PlayerState.ACTIVE)

    def test_set_state_invalid_type(self):
        """Test that setting a non-PlayerState value raises a TypeError."""
        with self.assertRaises(TypeError):
            self.player.set_state(1)

    def test_set_state_player_lost_invalid(self):
        """Test that a player who has lost cannot change their state."""
        self.player.set_state(PlayerState.LOST)
        with self.assertRaises(Exception):
            self.player.set_state(PlayerState.ACTIVE)

    def test_get_die_value(self):
        """Test that get_die_value returns the correct number of sides on the die."""
        self.assertEqual(self.player.get_die_value(), 6)
        self.assertNotEqual(self.player.get_die_value(), 5)

    def test_reset_roll_invalid(self):
        """Test that a player who has lost cannot reset their roll."""
        self.player.set_state(PlayerState.LOST)
        with self.assertRaises(Exception):
            self.player.reset_roll()

    def test_reset_roll_valid(self):
        """Test that resetting a roll clears the last_roll list."""
        self.player.reset_roll()
        self.assertEqual(self.player.last_roll, [])
