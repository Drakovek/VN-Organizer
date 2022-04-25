#!/usr/bin/env python3

from json import dump, load
from json.decoder import JSONDecodeError
from os.path import abspath
from re import sub
from typing import List

def get_color(color:str=None) -> str:
    """
    Returns the ANSI escape character for turning text a given color.
    If a valid color character is not given, sets to the default terminal color.

    :param color: Character representing color, defaults to None
    :type color: str, optional
    :return: ANSI color character
    :rtype: str
    """
    if color == "r":
        # Red
        return "\033[31m"
    elif color == "g":
        # Green
        return "\033[32m"
    elif color == "b":
        # Blue
        return "\033[34m"
    elif color == "c":
        # Cyan
        return "\033[36m"
    elif color == "m":
        # Magenta
        return "\033[35m"
    elif color == "y":
        # Bright Yellow
        return "\033[93m"
    else:
        # Default
        return "\033[0m"

def get_empty_branch_dict() -> dict:
    """
    Returns an empty dict for holding branch data.

    :return: Default dict for holding branch data.
    :rtype: dict
    """
    branch_dict = {"prompt":None,
                "response":None,
                "item_list":[],
                "branch":[],
                "end":False}
    return branch_dict

def add_item_to_dict(branch_dict:dict=None,
                item_type:str=None,
                text:str=None) -> dict:
    """
    Adds an item element to the item list in a branch dict.

    :param branch_dict: Branch dict to add item to, defaults to None
    :type branch_dict: dict, optional
    :param item_type: Type of item, defaults to None
    :type item_type: str, optional
    :param text: Text for the item, defaults to None
    :type text: str, optional
    :return: Given branch dict with item added
    :rtype: dict
    """
    try:
        # Get the list of items from the dict
        new_dict = branch_dict
        item_list = new_dict["item_list"]
        # Add event item to the dict
        if type(item_type) is str and type(text) is str:
            item = {"type":item_type, "text":text}
            item_list.append(item)
            new_dict["item_list"] = item_list
        # Return the dict with item added
        return new_dict
    except (KeyError, TypeError):
        return {}

def create_branch_in_dict(branch_dict:dict=None,
            prompt:str=None,
            responses:List[str]=None) -> dict:
    """
    Adds branch(es) to branch dict.

    :param branch_dict: Branch dict to add aditional branches to, defaults to None
    :type branch_dict: dict, optional
    :param prompt: Prompt or question for the branch split, defaults to None
    :type prompt: str, optional
    :param responses: String responses to the prompt, defaults to None
    :type responses: list[str], optional
    :return: Branch dict with added branches
    :rtype: dict
    """
    try:
        # Return the given dict if prompt is not valid
        if type(prompt) is not str or type(responses) is not list:
            return branch_dict
        # Create new branch dict for each response
        res_dicts = []
        new_dict = branch_dict
        for response in responses:
            res_dict = get_empty_branch_dict()
            res_dict["prompt"] = prompt
            res_dict["response"] = response
            res_dicts.append(res_dict)
        # Add branches to the original dict and return
        new_dict["branch"] = res_dicts
        new_dict["end"] = False
        return new_dict
    except TypeError:
        return {}

def get_dict_from_path(branch_dict:dict=None, path:List[int]=None) -> dict:
    """
    Returns the internal dict for a branch dict based on a given path.
    Path is a list of indexes indicating which option to pick in the "branch" key of the dict.

    :param branch_dict: Branch dict for getting sub dict within, defaults to None
    :type branch_dict: dict, optional
    :param path: Path of the sub dict to retrieve, defaults to None
    :type path: list[int], optional
    :return: Sub dict indicated by the path
    :rtype: dict
    """
    try:
        new_dict = branch_dict
        for branch in path:
            new_dict = new_dict["branch"][branch]
        return new_dict
    except (IndexError, KeyError, TypeError):
        return {}

def set_dict_from_path(branch_dict:dict=None,
            replace_dict:dict=None,
            path:List[int]=None) -> dict:
    """
    Sets the dict at a given path to the given dict.
    Path is a list of indexes indicating which option to pick in the "branch" key of the dict.
    
    :param branch_dict: Branch dict to modify, defaults to None
    :type branch_dict: dict, optional
    :param replace_dict: Dict with which to replace the dict at the given path, defaults to None
    :type replace_dict: dict, optional
    :param path: Path of the dict to replace, defaults to None
    :type path: list[int], optional
    :return: Branch dict with given path modified
    :rtype: dict
    """
    try:
        if len(path) == 0:
            return replace_dict
        new_dict = branch_dict
        sub_dict = branch_dict["branch"][path[0]]
        new_dict["branch"][path[0]] = set_dict_from_path(sub_dict, replace_dict, path[1:])
        return new_dict
    except (IndexError, TypeError):
        return branch_dict

def is_complete(branch_dict:dict=None) -> bool:
    """
    Returns whether a given branch and all it's sub-branches are marked as complete.

    :param branch_dict: Branch dict to check, defaults to None
    :type branch_dict: dict, optional
    :return: Whether the branch and all sub-branches are complete
    :rtype: bool
    """
    try:
        # Get internal branches
        branches = branch_dict["branch"]
        # Check if there are multiple branches
        if len(branches) == 0:
            # Return whether this single branch is finished
            return branch_dict["end"]
        else:
            # Check whether each sub branch is finished
            for branch in branches:
                if not is_complete(branch):
                    return False
        # Return True if all branches are found complete
        return True
    except (KeyError, TypeError):
        return False

def get_dict_print(branch_dict:dict=None, path:List[int]=None) -> str:
    """
    Gets printable text to show the user the contents of the branch dict at a given path.
    Path is a list of indexes indicating which option to pick in the "branch" key of the dict.

    :param branch_dict: Branch dict for getting sub dict within, defaults to None
    :type branch_dict: dict, optional
    :param path: Path of the sub dict to retrieve, defaults to None
    :type path: list[int], optional
    :return: Text to show the contents of the given dict at the given path
    :rtype: str
    """
    try:
        # Get the sub dict from the given path
        sub_dict = get_dict_from_path(branch_dict, path)
        # Get the item list
        text = ""
        item_list = sub_dict["item_list"]
        for item in item_list:
            if item["type"] == "s":
                line = get_color("c") + "(S) "
            else:
                line = get_color(item["type"].lower()) + "(E) "
            text = text + "\n" + line + item["text"] + get_color("d")
        # Add ending marker, if present
        if sub_dict["end"]:
            text = text + "\n[END]"
        # Get the next prompt and responses if available
        branches = sub_dict["branch"]
        if len(branches) > 0:
            text = text +  get_color("r") + "\n(P) " + branches[0]["prompt"] + get_color("d")
            for branch in branches:
                text = text + get_color("g") + "\n    ﹂" + branch["response"] + get_color("d")
        # Add tabs to text if necessary
        if len(path) > 0:
            text = text.replace("\n", "\n     ")
        text = sub("^\n", "", text)
        # Get the current response and prompt
        if sub_dict["response"] is not None and sub_dict["prompt"] is not None:
            text = get_color("g") + "    ﹂" + sub_dict["response"] + get_color("d") + "\n" + text
            text = get_color("r") + "(P) " + sub_dict["prompt"] + get_color("d") + "\n" + text
        # Get last save
        prev_dict = get_dict_from_path(branch_dict, path[:-1])
        if len(path) == 0:
            prev_dict = {"item_list":[]}
        item_list = prev_dict["item_list"]
        for i in range(len(item_list)-1, -1, -1):
            if item_list[i]["type"] == "s":
                text = get_color("c") + "(S) " + item_list[i]["text"] + get_color("d") + "\n" + text
                break
        # Add complete tag if the branch and all sub-branches are complete
        if is_complete(sub_dict):
            text = get_color("g") + "[COMPLETE BRANCH]" + get_color("d") + "\n" + text
        # Add elipses if not at the beginning of the branch
        if len(path) > 0:
            text = "(...)\n" + text
        # Return the formatted text
        text = sub("^\n+|\n+$", "", text)
        return text
    except (KeyError, TypeError):
        return ""

def write_branch_dict(file:str=None, branch_dict:dict=None):
    """
    Write a given branch dict as a JSON file with the given filename.

    :param file: File path to save JSON file to, defaults to None
    :type file: str, optional
    :param branch_dict: Dictionary to save as a JSON file, defaults to None
    :type branch_dict: dict, optional
    """
    try:
        # Test that the branch_dict is a proper dict
        assert type(branch_dict) is dict
        # Write dict as a JSON file
        with open(abspath(file), "w") as out_file:
            dump(branch_dict, out_file, indent=4, separators=(",", ": "))
    except (AssertionError, FileNotFoundError, TypeError): pass

def read_branch_dict(file:str=None) -> dict:
    """
    Reads a JSON file and converts to a branch dict.
    Returns None is keys of the dict do not match the branch dict format.

    :param file: File path of JSON file to read, defaults to None
    :type file: str, optional
    :return: Branch dict
    :rtype: dict
    """
    try:
        # Read given file as JSON
        with open(abspath(file)) as in_file:
            json = load(in_file)
        # Check if JSON is for a branch dict
        assert json["prompt"] is None or type(json["prompt"]) is str
        assert json["response"] is None or type(json["response"]) is str
        assert type(json["end"]) is bool
        assert type(json["item_list"]) is list
        assert type(json["branch"]) is list
        return json
    except (AssertionError, FileNotFoundError, JSONDecodeError, KeyError, TypeError):
        return None
