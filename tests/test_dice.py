"""
Tests that check the correctness of the Die class.

For example tests that check the correctness of the __init__ method,
the __str__ method, the roll method, and exceptions raised by the class.
"""

import unittest
from src.dice import Die


class TestDice(unittest.TestCase):
    """
    Test suite for the Die class that verifies dice creation, validation, and rolling.
    Tests include initialization with custom sides, rolling individual dice and multiple dice,
    and validation of input parameters.
    """
    def setUp(self):
        """Set up test fixtures, creating standard 6-sided and custom 10-sided dice."""
        self.die = Die(6)
        self.die2 = Die(10)

    def test_die_init_default(self):
        """Test that a die is initialized with 6 sides by default."""
        die = Die()
        self.assertEqual(die.sides, 6)

    def test_die_init_custom(self):
        """Test that a die can be initialized with a custom number of sides."""
        die = Die(10)
        self.assertEqual(die.sides, 10)

    def test_die_init_invalid_value(self):
        """Test that initialization fails with invalid (zero) number of sides."""
        with self.assertRaises(ValueError):
            Die(0)

    def test_die_init_invalid_type(self):
        """Test that initialization fails with non-numeric type for sides."""
        with self.assertRaises(TypeError):
            Die("10")

    def test_roll_standard(self):
        """Test that rolling a standard die returns a value within the valid range."""
        for _ in range(100):
            result = self.die.roll()
            self.assertTrue(1 <= result <= self.die.sides)

    def test_roll_custom_sides(self):
        """Test that rolling a die with custom sides returns a value within the valid range."""
        for _ in range(100):
            result = self.die2.roll()
            self.assertTrue(1 <= result <= self.die2.sides)

    def test_set_sides(self):
        """Test that the number of sides can be changed after initialization."""
        self.die.set_sides(10)
        self.assertEqual(self.die.sides, 10)

    def test_roll_dice_count(self):
        """Test that rolling multiple dice returns the correct number of results."""
        for _ in range(100):
            result = self.die.roll_dice(5)
            self.assertEqual(len(result), 5)

    def test_roll_dice_zero_dice(self):
        """Test that rolling zero dice raises a ValueError."""
        with self.assertRaises(ValueError):
            self.die.roll_dice(0)

    def test_roll_dice_invalid(self):
        """Test that rolling non-numeric dice count raises a TypeError."""
        with self.assertRaises(TypeError):
            self.die.roll_dice("5")

    def test_set_sides_invalid(self):
        """Test that setting invalid values or types for sides raises appropriate exceptions."""
        with self.assertRaises(ValueError):
            self.die.set_sides(0)
        with self.assertRaises(TypeError):
            self.die.set_sides("10")

    def test_str(self):
        """Test the string representation of dice with different sides."""
        self.assertEqual(str(self.die), "Die(6 sides)")
        self.assertEqual(str(self.die2), "Die(10 sides)")

    def tearDown(self):
        """Clean up test fixtures after test."""
        self.die = None
