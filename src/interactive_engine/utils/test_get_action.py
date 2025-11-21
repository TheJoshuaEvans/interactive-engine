import unittest

from interactive_engine.data_classes import Action, ActionType
from interactive_engine.strings import SystemStrings
from interactive_engine.utils.get_action import get_action

class TestGetAction(unittest.TestCase):
    """Unit tests for the get_action utility function."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock actions for testing
        self.look_scene_action = Action("You look around the scene.", ActionType.LOOK)
        self.look_door_action = Action("You examine the door closely.", ActionType.LOOK)
        self.look_window_action = Action("You look at the window.", ActionType.LOOK)
        self.move_north_action = Action("You move north.", ActionType.MOVE)
        self.move_south_action = Action("You move south.", ActionType.MOVE)
        self.take_key_action = Action("You take the key.", ActionType.TAKE)
        self.combine_key_and_door_action = Action("You combine the key and the door.", ActionType.COMBINE)
        self.inventory_action = Action("You check your inventory.", ActionType.INVENTORY)
        self.help_action = Action("Here's some help.", ActionType.HELP)
        self.exit_action = Action("You exit the game.", ActionType.EXIT)

        # Create a typical action dictionary structure
        self.action_dict = {
            ActionType.LOOK: {
                "scene": self.look_scene_action,
                "door": self.look_door_action,
                "window": self.look_window_action,
            },
            ActionType.MOVE: {
                "north": self.move_north_action,
                "south": self.move_south_action,
            },
            ActionType.TAKE: {
                "key": self.take_key_action,
            },
            ActionType.COMBINE: {
                "key and door": self.combine_key_and_door_action
            },
            ActionType.INVENTORY: self.inventory_action,  # Direct action (no target)
            ActionType.HELP: self.help_action,  # Direct action (no target)
            ActionType.EXIT: self.exit_action,  # Direct action (no target)
        }

    def test_get_action_with_target_lowercase(self):
        """Test getting an action with a lowercase target."""
        result = get_action("look door", self.action_dict)
        self.assertEqual(result, self.look_door_action)
        self.assertEqual(result.text, "You examine the door closely.")

    def test_get_action_with_target_uppercase(self):
        """Test getting an action with an uppercase command."""
        result = get_action("LOOK door", self.action_dict)
        self.assertEqual(result, self.look_door_action)

    def test_get_action_with_target_mixed_case(self):
        """Test getting an action with mixed case command and target."""
        result = get_action("LoOk DOOR", self.action_dict)
        self.assertEqual(result, self.look_door_action)

    def test_get_action_with_extra_whitespace(self):
        """Test getting an action with extra whitespace."""
        result = get_action("  look   door  ", self.action_dict)
        self.assertEqual(result, self.look_door_action)

    def test_get_action_with_multiple_word_target(self):
        """Test getting an action where target contains spaces."""
        # In this case, everything after the first space should be the target
        result = get_action("combine key and door", self.action_dict)
        # This should fail to find an action since "scene and more words" won't match
        with self.assertRaises(ValueError) as context:
            get_action("look scene and more words", self.action_dict)
        self.assertIn(SystemStrings.MISSING_ACTION_TEXT, str(context.exception))

    def test_get_action_direct_action_no_target(self):
        """Test getting a direct action without a target."""
        result = get_action("inventory", self.action_dict)
        self.assertEqual(result, self.inventory_action)
        self.assertEqual(result.text, "You check your inventory.")

    def test_get_action_direct_action_help(self):
        """Test getting the help direct action."""
        result = get_action("help", self.action_dict)
        self.assertEqual(result, self.help_action)

    def test_get_action_direct_action_exit(self):
        """Test getting the exit direct action."""
        result = get_action("exit", self.action_dict)
        self.assertEqual(result, self.exit_action)

    def test_get_action_direct_action_with_uppercase(self):
        """Test getting a direct action with uppercase."""
        result = get_action("INVENTORY", self.action_dict)
        self.assertEqual(result, self.inventory_action)

    def test_get_action_different_targets_same_type(self):
        """Test getting different actions of the same type."""
        result1 = get_action("look scene", self.action_dict)
        result2 = get_action("look door", self.action_dict)
        result3 = get_action("look window", self.action_dict)

        self.assertEqual(result1, self.look_scene_action)
        self.assertEqual(result2, self.look_door_action)
        self.assertEqual(result3, self.look_window_action)
        self.assertNotEqual(result1, result2)
        self.assertNotEqual(result2, result3)

    def test_get_action_invalid_action_type(self):
        """Test that an invalid action type raises ValueError."""
        with self.assertRaises(ValueError) as context:
            get_action("invalid door", self.action_dict)

        self.assertIn(SystemStrings.MISSING_ACTION_TEXT, str(context.exception))
        self.assertIn("Unknown action: invalid", str(context.exception))

    def test_get_action_missing_action_type_in_dict(self):
        """Test that a valid action type not in the dict raises ValueError."""
        with self.assertRaises(ValueError) as context:
            get_action("listen door", self.action_dict)

        self.assertIn(SystemStrings.MISSING_ACTION_TEXT, str(context.exception))
        self.assertIn("No actions of type: listen", str(context.exception))

    def test_get_action_missing_target_in_dict(self):
        """Test that a valid action type with invalid target raises ValueError."""
        with self.assertRaises(ValueError) as context:
            get_action("look nonexistent", self.action_dict)

        self.assertIn(SystemStrings.MISSING_ACTION_TEXT, str(context.exception))
        self.assertIn("No action found for target: nonexistent", str(context.exception))

    def test_get_action_empty_string(self):
        """Test that an empty string raises ValueError."""
        with self.assertRaises(ValueError) as context:
            get_action("", self.action_dict)

        self.assertIn(SystemStrings.MISSING_ACTION_TEXT, str(context.exception))

    def test_get_action_whitespace_only(self):
        """Test that whitespace-only input raises ValueError."""
        with self.assertRaises(ValueError) as context:
            get_action("   ", self.action_dict)

        self.assertIn(SystemStrings.MISSING_ACTION_TEXT, str(context.exception))

    def test_get_action_with_target_but_no_target_in_dict(self):
        """Test providing a target for a direct action."""
        action = get_action("inventory something", self.action_dict)

        self.assertEqual(action, self.inventory_action)

    def test_get_action_case_sensitive_targets(self):
        """Test that targets are case-insensitive."""
        result1 = get_action("look DOOR", self.action_dict)
        result2 = get_action("look door", self.action_dict)
        result3 = get_action("look DoOr", self.action_dict)

        self.assertEqual(result1, self.look_door_action)
        self.assertEqual(result2, self.look_door_action)
        self.assertEqual(result3, self.look_door_action)

    def test_get_action_empty_action_dict(self):
        """Test with an empty action dictionary."""
        empty_dict = {}

        with self.assertRaises(ValueError) as context:
            get_action("look door", empty_dict)

        self.assertIn(SystemStrings.MISSING_ACTION_TEXT, str(context.exception))
        self.assertIn("No actions of type: look", str(context.exception))

    def test_get_action_returns_correct_action_object(self):
        """Test that the returned action has the correct attributes."""
        result = get_action("move north", self.action_dict)

        self.assertIsInstance(result, Action)
        self.assertEqual(result.text, "You move north.")
        self.assertEqual(result, self.move_north_action)

    def test_get_action_multiple_spaces_between_action_and_target(self):
        """Test handling of multiple spaces between action and target."""
        action = get_action("look     door", self.action_dict)
        self.assertEqual(action, self.look_door_action)


if __name__ == '__main__':
    unittest.main()
