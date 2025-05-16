"""
Unit tests for the RoundHandler class.

Different tests are defined for different aspects of the RoundHandler class, including
round initialization, bid validation, challenge outcomes, and game state transitions.
"""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from src.bid import Bid
from src.round_handler import RoundHandler
from src.players import Player
from src.state import PlayerState


class TestRoundHandler(unittest.TestCase):
    """
    Test suite for the RoundHandler class that verifies round management, bid handling,
    player turns, and challenge resolution. Tests include round initialization, bid
    validation, challenge outcomes, and game state transitions between rounds.
    """
    def setUp(self):
        """Set up test fixtures, creating players and a round handler for testing."""
        self.player1 = Player("Jan", 5)
        self.player2 = Player("Kowalski", 5)
        self.player1.state = PlayerState.WAITING
        self.player2.state = PlayerState.WAITING
        self.round_handler = RoundHandler([self.player1, self.player2])

    def test_init_round_handler_invalid_list(self):
        """Test that initialization fails with non-list players input."""
        with self.assertRaises(TypeError):
            self.round_handler = RoundHandler(1)

    def test_init_round_handler_invalid_list_type(self):
        """Test that initialization fails with non-Player objects in the list."""
        with self.assertRaises(TypeError):
            self.round_handler = RoundHandler([1, 2])

    # Start round
    @patch.object(Player, "make_roll")
    def test_start_round_make_roll(self, mock_make_roll):
        """Test that starting a round calls make_roll for each player."""
        self.round_handler.start_round()
        self.assertEqual(mock_make_roll.call_count, 2)
        mock_make_roll.assert_any_call(5)

    @patch.object(Player, "set_state")
    def test_start_round_set_state(self, mock_set_state):
        """Test that starting a round sets the first player to ACTIVE state."""
        self.round_handler.start_round()
        mock_set_state.assert_called_once_with(PlayerState.ACTIVE)

    # Testing the current number of rounds
    def test_start_round_check_round_number_beginning(self):
        """Test that the round number is 1 when the first round starts."""
        self.round_handler.start_round()
        self.assertEqual(self.round_handler.round_number, 1)

    def test_start_round_check_round_number_after_one_round(self):
        """Test that the round number increments when a new round starts."""
        self.round_handler.start_round()
        self.round_handler.start_round()
        self.assertEqual(self.round_handler.round_number, 2)

    # Checking the current player
    def test_start_round_check_current_player(self):
        """Test that the current player is set to ACTIVE when a round starts."""
        self.round_handler.start_round()
        self.assertEqual(
            self.round_handler.players[self.round_handler.current_player_id].state,
            PlayerState.ACTIVE,
        )

    def test_start_round_check_current_bid(self):
        """Test that the current bid is None when a round starts."""
        self.round_handler.start_round()
        self.assertEqual(self.round_handler.current_bid, None)

    # Checking if the dice amount is correct
    def test_start_round_check_dice_count(self):
        """Test that the total dice count is calculated correctly."""
        self.round_handler.start_round()
        self.assertEqual(self.round_handler.dice_count, 10)

    # Checking if the player list is initialized correctly
    def test_start_round_check_players(self):
        """Test that the players list is maintained when a round starts."""
        self.round_handler.start_round()
        self.assertEqual(self.round_handler.players, [self.player1, self.player2])

    def test_start_round_check_players_state(self):
        """Test that players are set to correct states when a round starts."""
        self.round_handler.start_round()
        self.assertEqual(self.player1.state, PlayerState.ACTIVE)
        self.assertEqual(self.player2.state, PlayerState.WAITING)

    # Make bid
    def test_make_bid_invalid_type_name(self):
        """Test that make_bid fails with non-string player name."""
        with self.assertRaises(TypeError):
            self.round_handler.make_bid(1, 3, 4)

    def test_make_bid_invalid_type_quantity(self):
        """Test that make_bid fails with non-numeric quantity."""
        self.player1.state = PlayerState.ACTIVE
        with self.assertRaises(TypeError):
            self.round_handler.make_bid("Jan", "3", 4)

    def test_make_bid_invalid_type_value(self):
        """Test that make_bid fails with non-numeric value."""
        self.player1.state = PlayerState.ACTIVE
        with self.assertRaises(TypeError):
            self.round_handler.make_bid("Jan", 3, "4")

    def test_make_bid_invalid_quantity(self):
        """Test that make_bid fails with zero quantity."""
        self.player1.state = PlayerState.ACTIVE
        with self.assertRaises(ValueError):
            self.round_handler.make_bid("Jan", 0, 4)

    def test_make_bid_invalid_value(self):
        """Test that make_bid fails with zero value."""
        self.player1.state = PlayerState.ACTIVE
        with self.assertRaises(ValueError):
            self.round_handler.make_bid("Jan", 3, 0)

    def test_make_bid_invalid_player(self):
        """Test that make_bid fails with inactive player."""
        with self.assertRaises(ValueError):
            self.round_handler.make_bid("Kowalski", 3, 4)

    def test_make_bid_invalid_player_none(self):
        """Test that make_bid fails with None player name."""
        with self.assertRaises(TypeError):
            self.round_handler.make_bid(None, 3, 4)

    def test_make_bid_bid_lower_than_last(self):
        """Test that make_bid fails when the new bid is lower than the current bid."""
        self.player1.state = PlayerState.ACTIVE
        self.round_handler.current_bid = Bid(3, 4, self.player1)
        with self.assertRaises(ValueError):
            self.round_handler.make_bid("Jan", 2, 4)

    def test_make_bid_higher_than_max_dice_value(self):
        """Test that make_bid fails when the value exceeds the max die value."""
        self.player1.state = PlayerState.ACTIVE
        with self.assertRaises(ValueError):
            self.round_handler.make_bid("Jan", 3, 10)

    def test_make_bid_higher_than_max_dice_quantity(self):
        """Test that make_bid fails when the quantity exceeds the total dice count."""
        self.player1.state = PlayerState.ACTIVE
        with self.assertRaises(ValueError):
            self.round_handler.make_bid("Jan", 13, 4)

    def test_make_bid_bid_higher_than_last(self):
        """Test that make_bid succeeds when the new bid is higher than the current bid."""
        self.player1.state = PlayerState.ACTIVE
        self.round_handler.current_bid = Bid(3, 4, self.player1)
        self.round_handler.make_bid("Jan", 3, 5)
        self.assertEqual(self.round_handler.current_bid.value, 5)

    @patch.object(RoundHandler, "get_player_by_name")
    def test_make_bid_get_player_by_name(self, mock_get_player_by_name):
        """Test that make_bid calls get_player_by_name with the correct name."""
        mock_player = MagicMock(spec=Player)
        mock_player.get_die_value.return_value = 6
        mock_get_player_by_name.return_value = mock_player
        mock_player.state = PlayerState.ACTIVE
        self.round_handler.make_bid("Jan", 3, 4)
        mock_get_player_by_name.assert_called_once_with("Jan")

    # is higher bid
    def test_is_higher_bid_true_if_none(self):
        """Test that any bid is higher than None."""
        self.player1.state = PlayerState.ACTIVE
        self.assertTrue(self.round_handler.is_higher_bid(Bid(3, 4, self.player1), None))

    def test_is_higher_bid_true_if_higher_quantity(self):
        """Test that a bid with higher quantity is considered higher."""
        self.player1.state = PlayerState.ACTIVE
        self.round_handler.current_bid = Bid(3, 4, self.player1)
        self.assertTrue(
            self.round_handler.is_higher_bid(
                Bid(4, 4, self.player1), Bid(3, 4, self.player1)
            )
        )

    def test_is_higher_bid_true_if_higher_value(self):
        """Test that a bid with higher value is considered higher."""
        self.player1.state = PlayerState.ACTIVE
        self.round_handler.current_bid = Bid(3, 4, self.player1)
        self.assertTrue(
            self.round_handler.is_higher_bid(
                Bid(3, 5, self.player1), Bid(3, 4, self.player1)
            )
        )

    # next player
    def test_next_player_check_state(self):
        """Test that next_player updates player states correctly."""
        self.round_handler.next_player()
        self.assertEqual(self.player1.state, PlayerState.WAITING)
        self.assertEqual(self.player2.state, PlayerState.ACTIVE)

    def test_next_player_check_current_player_id(self):
        """Test that next_player updates the current_player_id correctly."""
        self.round_handler.next_player()
        self.assertEqual(self.round_handler.current_player_id, 1)

    def test_next_player_check_current_player_state(self):
        """Test that the new current player is set to ACTIVE state."""
        self.round_handler.next_player()
        self.assertEqual(
            self.round_handler.players[self.round_handler.current_player_id].state,
            PlayerState.ACTIVE,
        )

    # challenge and end round
    def test_challenge_and_end_round_invalid_player_name(self):
        """Test that challenge_and_end_round fails with non-string player name."""
        with self.assertRaises(TypeError):
            self.round_handler.challenge_and_end_round(10)

    def test_challenge_and_end_round_invalid_player_none(self):
        """Test that challenge_and_end_round fails with a player name that doesn't exist."""
        with self.assertRaises(ValueError):
            self.round_handler.challenge_and_end_round(self.player1.name)

    def test_challenge_and_end_round_invalid_player_not_active(self):
        """Test that challenge_and_end_round fails with inactive player."""
        with self.assertRaises(ValueError):
            self.round_handler.challenge_and_end_round(self.player2.name)

    def test_challenge_and_end_round_no_bid(self):
        """Test that challenge_and_end_round fails when there is no current bid."""
        self.round_handler.current_bid = None
        with self.assertRaises(ValueError) as context:
            self.round_handler.challenge_and_end_round("Player1")
        self.assertEqual(str(context.exception), "No bid to challenge")

    # challenge and end run
    @patch.object(RoundHandler, "get_player_by_name")
    def test_challenge_and_end_round_get_player_by_name(self, mock_get_player):
        """Test that challenge_and_end_round calls get_player_by_name with the correct name."""
        mock_bid = MagicMock()
        mock_bid.value = 4
        mock_bid.quantity = 3
        mock_bid.player = MagicMock(spec=Player)
        mock_bid.player.name = "Bidder"
        self.round_handler.current_bid = mock_bid

        player = MagicMock(spec=Player)
        player.name = "Challenger"
        player.state = PlayerState.ACTIVE
        mock_get_player.return_value = player

        self.round_handler.challenge_and_end_round("Challenger")
        mock_get_player.assert_called_once_with("Challenger")

    @patch.object(RoundHandler, "get_player_by_name")
    @patch.object(RoundHandler, "count_dice_value")
    def test_challenge_and_end_round_count_dice_value(
        self, mock_count_dice_value, mock_get_player
    ):
        """Test that challenge_and_end_round calls count_dice_value with the correct value."""
        mock_bid = MagicMock()
        mock_bid.quantity = 3
        mock_bid.value = 4
        mock_bid.player = MagicMock(spec=Player)
        self.round_handler.current_bid = mock_bid

        player = MagicMock(spec=Player)
        player.name = "Challenger"
        player.state = PlayerState.ACTIVE
        mock_get_player.return_value = player

        mock_count_dice_value.return_value = 5
        self.round_handler.challenge_and_end_round("Challenger")
        mock_count_dice_value.assert_called_once_with(4)

    @patch.object(RoundHandler, "resolve_challenge")
    @patch.object(RoundHandler, "get_player_by_name")
    @patch.object(RoundHandler, "count_dice_value")
    def test_challenge_and_end_round_resolve_challenge_called(
        self, mock_count_dice_value, mock_get_player, mock_resolve
    ):
        """Test that challenge_and_end_round calls resolve_challenge with correct parameters."""
        mock_bid = MagicMock()
        mock_bid.quantity = 3
        mock_bid.value = 4
        mock_bid.player = MagicMock(spec=Player)
        self.round_handler.current_bid = mock_bid

        challenger = MagicMock(spec=Player)
        challenger.name = "Challenger"
        challenger.state = PlayerState.ACTIVE
        mock_get_player.return_value = challenger

        mock_count_dice_value.return_value = 5

        mock_resolve.return_value = challenger

        self.round_handler.challenge_and_end_round("Challenger")
        mock_resolve.assert_called_once_with(mock_bid.player, challenger, 3, 5)

    @patch.object(RoundHandler, "apply_penalty")
    @patch.object(RoundHandler, "resolve_challenge")
    @patch.object(RoundHandler, "get_player_by_name")
    @patch.object(RoundHandler, "count_dice_value")
    def test_challenge_and_end_round_apply_penalty_called(
        self, mock_count_dice_value, mock_get_player, mock_resolve, mock_apply_penalty
    ):
        """Test that challenge_and_end_round calls apply_penalty with the loser of the challenge."""
        mock_bid = MagicMock()
        mock_bid.quantity = 3
        mock_bid.value = 4
        mock_bid.player = MagicMock(spec=Player)
        self.round_handler.current_bid = mock_bid

        challenger = MagicMock(spec=Player)
        challenger.name = "Challenger"
        challenger.state = PlayerState.ACTIVE
        mock_get_player.return_value = challenger

        mock_count_dice_value.return_value = 5
        mock_resolve.return_value = challenger

        self.round_handler.challenge_and_end_round("Challenger")
        mock_apply_penalty.assert_called_once_with(challenger)

    @patch.object(RoundHandler, "reset_players_after_round")
    @patch.object(RoundHandler, "resolve_challenge")
    @patch.object(RoundHandler, "get_player_by_name")
    @patch.object(RoundHandler, "count_dice_value")
    def test_challenge_and_end_round_reset_players_after_round_called(
        self, mock_count, mock_get_player, mock_resolve, mock_reset
    ):
        """Test that challenge_and_end_round calls reset_players_after_round."""
        mock_bid = MagicMock()
        mock_bid.quantity = 3
        mock_bid.value = 4
        mock_bid.player = MagicMock(spec=Player)
        self.round_handler.current_bid = mock_bid

        challenger = MagicMock(spec=Player)
        challenger.name = "Challenger"
        challenger.state = PlayerState.ACTIVE
        mock_get_player.return_value = challenger

        mock_count.return_value = 5
        mock_resolve.return_value = challenger

        self.round_handler.challenge_and_end_round("Challenger")
        mock_reset.assert_called_once()

    @patch.object(RoundHandler, "start_round")
    @patch.object(RoundHandler, "check_if_start_next_round")
    @patch.object(RoundHandler, "resolve_challenge")
    @patch.object(RoundHandler, "get_player_by_name")
    @patch.object(RoundHandler, "count_dice_value")
    def test_challenge_and_end_round_starts_new_round_called(
        self, mock_count, mock_get_player, mock_resolve, mock_check, mock_start
    ):
        """Test that challenge_and_end_round starts a new round when there are enough players."""
        mock_check.return_value = True

        mock_bid = MagicMock()
        mock_bid.quantity = 3
        mock_bid.value = 4
        mock_bid.player = MagicMock(spec=Player)
        self.round_handler.current_bid = mock_bid

        challenger = MagicMock(spec=Player)
        challenger.state = PlayerState.ACTIVE
        challenger.name = "Challenger"
        mock_get_player.return_value = challenger
        mock_resolve.return_value = challenger
        mock_count.return_value = 5

        self.round_handler.challenge_and_end_round("Challenger")

        mock_start.assert_called_once()

    @patch.object(RoundHandler, "end_game_info")
    @patch.object(RoundHandler, "check_if_start_next_round")
    @patch.object(RoundHandler, "resolve_challenge")
    @patch.object(RoundHandler, "get_player_by_name")
    @patch.object(RoundHandler, "count_dice_value")
    def test_challenge_and_end_round_ends_game_when_needed(
        self, mock_count, mock_get_player, mock_resolve, mock_check, mock_end_game
    ):
        """Test that challenge_and_end_round ends the game when there are not enough players."""
        mock_check.return_value = False

        mock_bid = MagicMock()
        mock_bid.quantity = 3
        mock_bid.value = 4
        mock_bid.player = MagicMock(spec=Player)
        self.round_handler.current_bid = mock_bid

        challenger = MagicMock(spec=Player)
        challenger.name = "Challenger"
        challenger.state = PlayerState.ACTIVE
        mock_get_player.return_value = challenger
        mock_resolve.return_value = challenger
        mock_count.return_value = 5

        self.round_handler.challenge_and_end_round("Challenger")

        mock_end_game.assert_called_once()

    # test that checks if all the method calls in reset players after round run correctly
    @patch.object(RoundHandler, "eliminate_player")
    def test_reset_players_after_round(self, mock_eliminate):
        """Test that reset_players_after_round eliminates
         players with zero dice and resets others."""
        player1 = MagicMock(spec=Player)
        player1.reset_roll = MagicMock()
        player1.get_dice_count.return_value = 0
        player1.state = PlayerState.ACTIVE

        player2 = MagicMock(spec=Player)
        player2.reset_roll = MagicMock()
        player2.get_dice_count.return_value = 2
        player2.state = PlayerState.WAITING

        self.round_handler.players = [player1, player2]

        self.round_handler.reset_players_after_round()

        mock_eliminate.assert_called_once_with(player1)

        player1.reset_roll.assert_called_once()
        player2.reset_roll.assert_called_once()

        player1.set_state.assert_not_called()
        player2.set_state.assert_called_once_with(PlayerState.WAITING)

    def test_reset_players_after_round_no_players(self):
        """Test that reset_players_after_round handles empty player list."""
        self.round_handler.players = []
        self.round_handler.reset_players_after_round()

    def test_reset_players_after_round_no_active_players(self):
        """Test that reset_players_after_round handles players with no active state."""
        player1 = MagicMock(spec=Player)
        player1.reset_roll = MagicMock()
        player1.get_dice_count.return_value = 0
        player1.state = PlayerState.WAITING

        player2 = MagicMock(spec=Player)
        player2.reset_roll = MagicMock()
        player2.get_dice_count.return_value = 2
        player2.state = PlayerState.WAITING

        player1.assert_not_called()
        player2.assert_not_called()

    # check if start next round
    def test_check_if_start_next_round_with_enough_players(self):
        """Test that check_if_start_next_round returns True when there are enough active players."""
        self.player1.state = PlayerState.WAITING
        self.player2.state = PlayerState.WAITING
        self.assertTrue(self.round_handler.check_if_start_next_round())

    def test_check_if_start_next_round_with_not_enough_players(self):
        """Test that check_if_start_next_round returns False
         when there are not enough active players."""
        self.player1.state = PlayerState.WAITING
        self.player2.state = PlayerState.LOST
        self.assertFalse(self.round_handler.check_if_start_next_round())

    # check count dice value checking if dice value is calculated correctly
    def test_count_dice_value_with_valid_dice_value(self):
        """Test that count_dice_value correctly counts dice with the specified value."""
        player1 = MagicMock(spec=Player)
        player1.last_roll = [1, 1, 2]
        player1.get_die_value.return_value = 6
        player2 = MagicMock(spec=Player)
        player2.last_roll = [1, 3, 4]
        player2.get_die_value.return_value = 6
        self.round_handler.players = [player1, player2]
        self.round_handler.current_player_id = 0
        count = self.round_handler.count_dice_value(1)
        self.assertEqual(count, 3)

    def test_count_dice_value_with_invalid_value(self):
        """Test that count_dice_value fails with non-numeric value."""
        with self.assertRaises(ValueError):
            self.round_handler.count_dice_value("10")

    def test_count_dice_value_with_invalid_dice_value(self):
        """Test that count_dice_value fails with value outside the range of a die."""
        with self.assertRaises(ValueError):
            self.round_handler.count_dice_value(13)

    # apply penalty
    @patch.object(RoundHandler, "eliminate_player")
    def test_apply_penalty_with_valid_player(self, mock_eliminate):
        """Test that apply_penalty reduces a player's dice and doesn't
         eliminate them if they have dice left."""
        player = MagicMock(spec=Player)
        player.name = "Player"
        player.get_dice_count.return_value = 2

        self.round_handler.apply_penalty(player)

        player.lose_die.assert_called_once()

        mock_eliminate.assert_not_called()

    @patch.object(RoundHandler, "eliminate_player")
    def test_apply_penalty_with_zero_dice(self, mock_eliminate):
        """Test that apply_penalty eliminates a player if they have zero dice left."""
        player = MagicMock(spec=Player)
        player.name = "Player"
        player.get_dice_count.return_value = 0

        self.round_handler.apply_penalty(player)

        mock_eliminate.assert_called_once_with(player)

    def test_apply_penalty_with_invalid_player(self):
        """Test that apply_penalty fails with non-Player object."""
        with self.assertRaises(Exception):
            self.round_handler.apply_penalty("Player")

    # test get player by name
    def test_get_player_by_name_with_valid_name(self):
        """Test that get_player_by_name returns the correct player for a valid name."""
        self.assertEqual(self.round_handler.get_player_by_name("Jan"), self.player1)
        self.assertEqual(
            self.round_handler.get_player_by_name("Kowalski"), self.player2
        )

    def test_get_player_by_name_that_doesnt_exist(self):
        """Test that get_player_by_name raises an exception for a player name that doesn't exist."""
        with self.assertRaises(Exception):
            self.round_handler.get_player_by_name("InvalidPlayer")

    def test_get_player_by_name_with_invalid_type(self):
        """Test that get_player_by_name fails with non-string name."""
        with self.assertRaises(TypeError):
            self.round_handler.get_player_by_name(10)

    def test_eliminate_player(self):
        """Test that eliminate_player sets a player's state to LOST."""
        self.round_handler.eliminate_player(self.player1)
        self.assertEqual(self.player1.state, PlayerState.LOST)

    def test_eliminate_player_with_invalid_player(self):
        """Test that eliminate_player fails with non-Player object."""
        with self.assertRaises(Exception):
            self.round_handler.eliminate_player("Player")

    # test resolve challenge
    def test_resolve_challenge_with_valid_players(self):
        """Test that resolve_challenge
         correctly determines the loser based on bid and actual dice count."""
        self.assertEqual(
            self.round_handler.resolve_challenge(self.player1, self.player2, 3, 5),
            self.player2,
        )
        self.assertEqual(
            self.round_handler.resolve_challenge(self.player1, self.player2, 5, 3),
            self.player1,
        )

    def test_resolve_challenge_with_invalid_players(self):
        """Test that resolve_challenge fails with non-Player objects."""
        with self.assertRaises(Exception):
            self.round_handler.resolve_challenge("a", self.player2, 3, 5)
        with self.assertRaises(Exception):
            self.round_handler.resolve_challenge(self.player1, "b", 3, 5)

    def test_resolve_challenge_with_invalid_dice_value(self):
        """Test that resolve_challenge fails with non-numeric bid quantity or count."""
        with self.assertRaises(TypeError):
            self.round_handler.resolve_challenge(self.player1, self.player2, "3", 10)
        with self.assertRaises(TypeError):
            self.round_handler.resolve_challenge(self.player1, self.player2, 3, "10")

    # get_active_player
    def test_get_active_player(self):
        """Test that get_active_player returns the currently active player."""
        self.round_handler.start_round()
        self.assertEqual(self.round_handler.get_active_player(), self.player1)

    def test_get_active_player_no_players(self):
        """Test that get_active_player raises an exception when there are no players."""
        self.round_handler.players = []
        with self.assertRaises(Exception):
            self.round_handler.get_active_player()

    def test_end_game_info(self):
        """Test that end_game_info returns the name of the last non-LOST player."""
        self.player1.state = PlayerState.LOST
        self.assertEqual(self.round_handler.end_game_info(), self.player2.name)

    def test_end_game_info_no_players(self):
        """Test that end_game_info raises an exception when there are no players."""
        self.round_handler.players = []
        with self.assertRaises(Exception):
            self.round_handler.end_game_info()

    def tearDown(self):
        """Clean up test fixtures after test."""
        self.round_handler = None
