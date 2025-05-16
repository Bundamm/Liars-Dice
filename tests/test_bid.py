"""
Tests that check the correctness of the Bid class.

For example, tests that check the correctness of the __init__ method,
the __eq__ method, and the __str__ method.
"""

import unittest
from src.bid import Bid
from src.players import Player
from src.state import PlayerState


class TestBid(unittest.TestCase):
    """
    Test suite for the Bid class that verifies bid creation, validation, and comparison.
    Tests include input validation, object equality, and string representation.
    """

    def setUp(self):
        """Set up test fixtures, creating players for use in tests."""
        self.player1 = Player("Jan", 5)
        self.player2 = Player("Kowalski", 5)
        self.player1.state = PlayerState.ACTIVE
        self.player2.state = PlayerState.WAITING

    def test_bid_init_positive(self):
        """Test that a bid is initialized correctly with valid inputs."""
        bid = Bid(3, 6, self.player1)
        self.assertEqual(bid.player, self.player1)
        self.assertEqual(bid.quantity, 3)
        self.assertEqual(bid.value, 6)

    def test_bid_init_negative(self):
        """Test that initialization fails with negative values for quantity or value."""
        with self.assertRaises(ValueError):
            Bid(-3, 6, self.player1)
        with self.assertRaises(ValueError):
            Bid(3, -6, self.player1)

    def test_bid_invalid_types(self):
        """Test that initialization fails with invalid types for the player parameter."""
        with self.assertRaises(TypeError):
            Bid(3, 6, 10)
        with self.assertRaises(TypeError):
            Bid(3, 6, None)

    def test_bid_invalid_values(self):
        """Test that initialization fails with zero or non-numeric values."""
        with self.assertRaises(ValueError):
            Bid(0, 3, self.player1)
        with self.assertRaises(ValueError):
            Bid(3, 0, self.player1)
        with self.assertRaises(ValueError):
            Bid("10", "20", self.player1)

    def test_bid_equality(self):
        """Test that two bids with the same attributes are considered equal."""
        bid1 = Bid(3, 6, self.player1)
        bid2 = Bid(3, 6, self.player1)
        self.assertEqual(bid1, bid2)

    def test_bid_str(self):
        """Test the string representation of a bid includes correct information."""
        bid = Bid(2, 4, self.player1)
        self.assertIn("2", str(bid))
        self.assertIn("4", str(bid))
        self.assertIn(self.player1.name, str(bid))

    def test_non_equality(self):
        """Test that bids with different attributes are not equal."""
        bid1 = Bid(3, 6, self.player1)
        bid2 = Bid(4, 6, self.player1)
        self.assertNotEqual(bid1, bid2)

    def test_get_player_name(self):
        """Test that get_player_name returns the correct player name."""
        bid = Bid(2, 5, self.player1)
        self.assertEqual(bid.get_player_name(), "Jan")

    def test_str(self):
        """Test the exact formatting of the string representation."""
        bid = Bid(2, 4, self.player1)
        self.assertEqual(str(bid), "Bid(2, 4, Jan)")

    def test_inactive_player(self):
        """Test that creating a bid with an inactive player raises a ValueError."""
        with self.assertRaises(ValueError):
            Bid(3, 6, self.player2)

    def test_higher_bid(self):
        """Test the greater than comparison for bids."""
        bid1 = Bid(3, 6, self.player1)
        bid2 = Bid(4, 6, self.player1)
        bid3 = Bid(2, 5, self.player1)
        bid4 = Bid(2, 4, self.player1)
        self.assertTrue(bid2 > bid1)
        self.assertTrue(bid2 > bid3)
        self.assertTrue(bid3 > bid4)

    def test_higher_bid_wrong_type(self):
        """Test that the greater than comparison raises a TypeError when compared to a non-bid."""
        bid = Bid(3, 6, self.player1)
        with self.assertRaises(TypeError):
            bid > 3

    def test_lower_bid_wrong_type(self):
        """Test that the lower than comparison raises a TypeError when compared to a non-bid."""
        bid = Bid(3, 6, self.player1)
        with self.assertRaises(TypeError):
            bid < 3
