from interactive_engine.data_classes import Action, ActionType
from interactive_engine.strings import SystemStrings

def get_action(in_text: str, action_dict: dict) -> Action:
    """
    Utility function to get an Action from an input string and action dictionary.

    Args:
        in_text (str): The input text to match against action keywords
        action_dict (dict): The dictionary of actions to search
    Returns:
        action (Action): The matched Action, will throw an error if no action is found
    """
    # Split the run string using the first space to get the action and target
    parts = in_text.strip().split(' ', 1)
    action_str = parts[0].strip()
    target_str = parts[1].strip() if len(parts) > 1 else ''

    # Get the action type from the action string
    action_type = ActionType._value2member_map_.get(action_str.lower()) # type: ActionType # type: ignore
    if (not action_type):
        raise ValueError(SystemStrings.MISSING_ACTION_TEXT + f" (Unknown action: {action_str})")

    # Get the action dictionary for the action type, or any direct action of that type (if there is no target)
    action_or_dict = action_dict.get(action_type)
    if (not action_or_dict):
        raise ValueError(SystemStrings.MISSING_ACTION_TEXT + f" (No actions of type: {action_type.value})")

    # Get the exact action for the target string, or use the action directly if it's a direct action (with no target)
    if isinstance(action_or_dict, Action):
        action = action_or_dict
    else:
        action = action_or_dict.get(target_str.lower())

    if not action:
        raise ValueError(SystemStrings.MISSING_ACTION_TEXT + f" (No action found for target: {target_str})")

    return action
