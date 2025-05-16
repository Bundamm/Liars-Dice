"""
Tests that check the correctness of the GameHandler class.

For example, tests that check if the correct exception is raised when a player
tries to make a bid when they are not active, or that the correct player is
chosen to challenge when there is a tie, are included here.
"""

import unittest
from unittest.mock import patch

from src.bid import Bid
from src.game_handler import GameHandler

from src.round_handler import RoundHandler
from src.state import PlayerState


class TestGameHandler(unittest.TestCase):
    """
    Test suite for the GameHandler class that verifies game setup, player management,
    game state transitions, and turn actions. Tests include initialization, player creation,
    bidding, challenging, and game/round progression management.
    """
    def setUp(self):
        """Set up test fixtures, creating a game with two players and three dice each."""
        self.game = GameHandler(["Player1", "Player2"], 3)

    def test_init_game_handler_invalid_number_of_dice_type(self):
        """Test that initialization fails with non-numeric dice count."""
        with self.assertRaises(TypeError):
            self.game = GameHandler(["Player1", "Player2"], "3")

    def test_init_game_handler_invalid_number_of_dice(self):
        """Test that initialization fails with zero or negative dice count."""
        with self.assertRaises(ValueError):
            self.game = GameHandler(["Player1", "Player2"], 0)
        with self.assertRaises(ValueError):
            self.game = GameHandler(["Player1", "Player2"], -1)

    def test_init_game_handler_valid(self):
        """Test that a game is initialized correctly with valid inputs."""
        self.assertEqual(self.game.players_names, ["Player1", "Player2"])
        self.assertEqual(self.game.dice_count, 3)

    def test_create_players_valid(self):
        """Test that players are created correctly with valid inputs."""
        self.game.create_players(["Player1", "Player2"])
        self.assertEqual(len(self.game.players), 2)
        self.assertEqual(self.game.players[0].name, "Player1")
        self.assertEqual(self.game.players[1].name, "Player2")
        self.assertEqual(self.game.players[0].get_dice_count(), 3)
        self.assertEqual(self.game.players[1].get_dice_count(), 3)

    def test_create_players_invalid_list(self):
        """Test that player creation fails with non-list input or non-string names."""
        with self.assertRaises(TypeError):
            self.game.create_players(1)
        with self.assertRaises(TypeError):
            self.game.create_players([1, 2])

    def test_play_bid_turn(self):
        """Test that a player can make a valid bid during their turn."""
        player1 = self.game.players[0]
        player1.state = PlayerState.ACTIVE
        self.game.play_bid_turn(player1, 2, 3)
        self.assertEqual(self.game.round_handler.current_bid.quantity, 2)
        self.assertEqual(self.game.round_handler.current_bid.value, 3)
        self.assertEqual(self.game.round_handler.current_bid.player.name, "Player1")

    def test_play_bid_turn_invalid_type_player(self):
        """Test that bidding fails with non-Player objects or player name strings."""
        with self.assertRaises(TypeError):
            self.game.play_bid_turn(1, 2, 3)
        with self.assertRaises(TypeError):
            self.game.play_bid_turn("Player1", 2, 3)

    def test_play_bid_turn_invalid_type_quantity_and_value(self):
        """Test that bidding fails with non-numeric quantity or value."""
        with self.assertRaises(TypeError):
            self.game.play_bid_turn(self.game.players[0], "2", 3)
        with self.assertRaises(TypeError):
            self.game.play_bid_turn(self.game.players[0], 2, "3")

    # test checking if in the right circumstances player one loses challenge
    @patch.object(RoundHandler, "challenge_and_end_round")
    def test_play_challenge(self, mock_challenge):
        """Test that a player can challenge the current bid and get the correct result."""
        player1 = self.game.players[0]
        player1.state = PlayerState.ACTIVE
        player2 = self.game.players[1]
        player2.state = PlayerState.WAITING

        self.game.round_handler.current_bid = Bid(2, 3, player1)
        mock_challenge.return_value = player1
        result = self.game.play_challenge_turn(player1)
        mock_challenge.assert_called_once_with(player1.name)
        self.assertEqual(result, player1)

    def test_play_challenge_invalid_type(self):
        """Test that challenging fails with non-Player objects or player name strings."""
        with self.assertRaises(TypeError):
            self.game.play_challenge_turn(1)
        with self.assertRaises(TypeError):
            self.game.play_challenge_turn("Player1")

    def test_play_challenge_invalid_state(self):
        """Test that challenging fails when the player is not active."""
        with self.assertRaises(Exception):
            self.game.play_challenge_turn(self.game.players[0])

    def test_play_check_turn(self):
        """Test that a player can check their dice during their turn."""
        player1 = self.game.players[0]
        player1.state = PlayerState.ACTIVE
        self.assertEqual(self.game.play_check_turn(player1), player1.last_roll)

    def test_play_check_turn_invalid_type(self):
        """Test that checking fails with non-Player objects or player name strings."""
        with self.assertRaises(TypeError):
            self.game.play_check_turn(1)
        with self.assertRaises(TypeError):
            self.game.play_check_turn("Player1")

    def test_play_check_turn_invalid_state(self):
        """Test that checking fails when the player is not active."""
        with self.assertRaises(Exception):
            self.game.play_check_turn(self.game.players[0])

    def test_get_active_players(self):
        """Test that get_active_player returns the currently active player."""
        player1 = self.game.players[0]
        player1.state = PlayerState.ACTIVE
        player2 = self.game.players[1]
        player2.state = PlayerState.WAITING
        self.assertEqual(self.game.get_active_player(), player1)

    def test_get_active_players_no_active(self):
        """Test that get_active_player raises an exception when no player is active."""
        player1 = self.game.players[0]
        player1.state = PlayerState.WAITING
        with self.assertRaises(Exception):
            self.game.get_active_player()

    def test_start_round(self):
        """Test that starting a round initializes the correct game state."""
        player1 = self.game.players[0]
        player2 = self.game.players[1]
        self.game.start_round()
        self.assertEqual(self.game.round_handler.current_bid, None)
        self.assertEqual(player1.state, PlayerState.ACTIVE)
        self.assertEqual(player2.state, PlayerState.WAITING)

    def test_get_round_number(self):
        """Test that get_round_number returns the correct round number."""
        self.game.start_round()
        self.assertEqual(self.game.get_round_number(), 1)

    def test_get_current_bid(self):
        """Test that get_current_bid returns the current bid in the round."""
        player1 = self.game.players[0]
        player1.state = PlayerState.ACTIVE
        self.game.round_handler.current_bid = Bid(2, 3, player1)
        self.assertEqual(
            self.game.get_current_bid(), self.game.round_handler.current_bid
        )

    def test_check_if_start_next_round_two_players(self):
        """Test that the game continues to the next round when there are multiple active players."""
        player1 = self.game.players[0]
        player1.state = PlayerState.ACTIVE
        player2 = self.game.players[1]
        player2.state = PlayerState.WAITING
        self.assertTrue(self.game.check_if_start_next_round())

    def test_check_if_start_next_round_one_player(self):
        """Test that the game ends when only one player remains active."""
        player1 = self.game.players[0]
        player1.state = PlayerState.ACTIVE
        player2 = self.game.players[1]
        player2.state = PlayerState.LOST
        self.assertFalse(self.game.check_if_start_next_round())

    def test_end_game_info(self):
        """Test that end_game_info returns the name of the winning player."""
        player1 = self.game.players[0]
        player1.state = PlayerState.LOST
        player2 = self.game.players[1]
        player2.state = PlayerState.ACTIVE
        self.assertEqual(self.game.end_game_info(), player2.name)

    def tearDown(self):
        """Clean up test fixtures after test."""
        self.game = None
