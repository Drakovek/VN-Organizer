#!/usr/bin/env python3

from json import dump
from os import mkdir
from os.path import abspath, exists, join
from tempfile import gettempdir
from shutil import rmtree
from vn_organizer.main.vn_organizer import add_item_to_dict
from vn_organizer.main.vn_organizer import create_branch_in_dict
from vn_organizer.main.vn_organizer import is_complete
from vn_organizer.main.vn_organizer import get_color
from vn_organizer.main.vn_organizer import get_dict_from_path
from vn_organizer.main.vn_organizer import get_dict_print
from vn_organizer.main.vn_organizer import get_empty_branch_dict
from vn_organizer.main.vn_organizer import read_branch_dict
from vn_organizer.main.vn_organizer import set_dict_from_path
from vn_organizer.main.vn_organizer import write_branch_dict

def get_test_dir() -> str:
    """
    Creates and returns test directory.

    :return: File path of the test directory
    :rtype: str
    """
    test_dir = abspath(join(abspath(gettempdir()), "vn_organizer_test"))
    if(exists(test_dir)):
        rmtree(test_dir)
    mkdir(test_dir)
    return test_dir

def test_get_color():
    """
    Tests the get_color function.
    """
    # Test getting color escape values
    assert get_color("r") == "\033[31m"
    assert get_color("g") == "\033[32m"
    assert get_color("b") == "\033[34m"
    assert get_color("c") == "\033[36m"
    assert get_color("m") == "\033[35m"
    assert get_color("y") == "\033[93m"
    assert get_color("d") == "\033[0m"
    # Test getting invalid color
    assert get_color(None) == "\033[0m"
    assert get_color("blah") == "\033[0m"
    assert get_color("") == "\033[0m"
    assert get_color() == "\033[0m"

def test_get_empty_branch_dict():
    """
    Tests the get_empty_branch_dict function.
    """
    branch_dict = get_empty_branch_dict()
    assert branch_dict["prompt"] is None
    assert branch_dict["response"] is None
    assert branch_dict["item_list"] == []
    assert branch_dict["branch"] == []
    assert branch_dict["end"] == False

def test_add_item_to_dict():
    """
    Tests the add_item_to_dict function.
    """
    # Test adding items to the item list in a branch dict
    branch_dict = get_empty_branch_dict()
    branch_dict["prompt"] = "Test?"
    branch_dict["response"] = "Yes"
    new_dict = add_item_to_dict(branch_dict, "s", "12-1")
    assert new_dict["prompt"] == "Test?"
    assert new_dict["response"] == "Yes"
    item_list = new_dict["item_list"]
    assert len(item_list) == 1
    assert item_list[0]["type"] == "s"
    assert item_list[0]["text"] == "12-1"
    # Test adding more items
    new_dict = add_item_to_dict(new_dict, "e", "An event")
    item_list = new_dict["item_list"]
    assert len(item_list) == 2
    assert item_list[0]["type"] == "s"
    assert item_list[0]["text"] == "12-1"
    assert item_list[1]["type"] == "e"
    assert item_list[1]["text"] == "An event"
    # Test adding items with invalid parameters
    assert add_item_to_dict(None, "s", "Thing") == {}
    assert add_item_to_dict({}, "s", "Thing") == {}
    new_dict = add_item_to_dict(new_dict, None, "Thing")
    assert len(new_dict["item_list"]) == 2
    new_dict = add_item_to_dict(new_dict, "s", None)
    assert len(new_dict["item_list"]) == 2
    new_dict = add_item_to_dict(new_dict, 2, "Thing")
    assert len(new_dict["item_list"]) == 2
    new_dict = add_item_to_dict(new_dict, "s", 3)
    assert len(new_dict["item_list"]) == 2

def test_create_branch_in_dict():
    """
    Tests the create_branch_in_dict function.
    """
    # Test adding branches to a given branch dict
    branch_dict = get_empty_branch_dict()
    branch_dict["prompt"] = "Test?"
    branch_dict["response"] = "Sure"
    branch_dict["end"] = True
    new_dict = create_branch_in_dict(branch_dict, "What do you think?", ["Yes", "No"])
    assert new_dict["prompt"] == "Test?"
    assert new_dict["response"] == "Sure"
    assert new_dict["item_list"] == []
    assert len(new_dict["branch"]) == 2
    assert new_dict["branch"][0]["prompt"] == "What do you think?"
    assert new_dict["branch"][1]["prompt"] == "What do you think?"
    assert new_dict["branch"][0]["response"] == "Yes"
    assert new_dict["branch"][1]["response"] == "No"
    assert not new_dict["end"]
    # Test adding branches with invalid parameters
    assert create_branch_in_dict(None, "question", ["y", "n"]) == {}
    branch_dict = get_empty_branch_dict()
    assert len(create_branch_in_dict(branch_dict, None, ["y", "n"])["branch"]) == 0
    assert len(create_branch_in_dict(branch_dict, "Question", None)["branch"]) == 0
    assert len(create_branch_in_dict(branch_dict, "Question", [])["branch"]) == 0

def test_get_dict_from_path():
    """
    Tests the get_dict_from_path function.
    """
    # Create branch dict for testing
    branch_dict = get_empty_branch_dict()
    branch_dict["prompt"] = "First"
    branch_dict = create_branch_in_dict(branch_dict, "Question", ["Yes", "No", "Maybe"])
    sub_dict = get_empty_branch_dict()
    sub_dict = create_branch_in_dict(sub_dict, "Other", ["Some", "Options"])
    branch_dict["branch"][1]["branch"] = [sub_dict]
    # Test getting sub-dicts using paths
    path_dict = get_dict_from_path(branch_dict, [])
    assert path_dict["prompt"] == "First"
    assert len(path_dict["branch"]) == 3
    path_dict = get_dict_from_path(branch_dict, [0])
    assert path_dict["prompt"] == "Question"
    assert path_dict["response"] == "Yes"
    assert len(path_dict["branch"]) == 0
    path_dict = get_dict_from_path(branch_dict, [1, 0, 1])
    assert path_dict["prompt"] == "Other"
    assert path_dict["response"] == "Options"
    assert len(path_dict["branch"]) == 0
    # Test using invalid parameters
    assert get_dict_from_path(branch_dict, [4]) == {}
    assert get_dict_from_path(branch_dict, [0, 1, 0, 0, 0, 0]) == {}
    assert get_dict_from_path(None, [0]) == {}
    assert get_dict_from_path({}, [0]) == {}

def test_set_dict_from_path():
    """
    Tests the set_dict_from_path function.
    """
    # Create branch dict for testing
    branch_dict = get_empty_branch_dict()
    branch_dict["prompt"] = "First"
    branch_dict = create_branch_in_dict(branch_dict, "Question", ["Yes", "No", "Maybe"])
    sub_dict = get_empty_branch_dict()
    sub_dict = create_branch_in_dict(sub_dict, "Other", ["Some", "Options"])
    branch_dict["branch"][1]["branch"] = [sub_dict]
    # Test setting a dict at a given path
    new_dict = get_empty_branch_dict()
    new_dict["prompt"] = "New"
    branch_dict = set_dict_from_path(branch_dict, new_dict, [0])
    return_dict = get_dict_from_path(branch_dict, [])
    assert return_dict["prompt"] == "First"
    assert len(return_dict["branch"]) == 3
    return_dict = get_dict_from_path(branch_dict, [0])
    assert return_dict["prompt"] == "New"
    # Test setting a dict multiple levels in
    new_dict = get_empty_branch_dict()
    new_dict["prompt"] = "Sub dict"
    new_dict["response"] = "Yep"
    branch_dict = set_dict_from_path(branch_dict, new_dict, [1, 0, 1])
    return_dict = get_dict_from_path(branch_dict, [1, 0, 1])
    assert return_dict["prompt"] == "Sub dict"
    assert return_dict["response"] == "Yep"
    return_dict = get_dict_from_path(branch_dict, [1, 0, 0])
    assert return_dict["prompt"] == "Other"
    assert return_dict["response"] == "Some"
    return_dict = get_dict_from_path(branch_dict, [0])
    assert return_dict["prompt"] == "New"
    # Test setting a dict at the base level
    new_dict = get_empty_branch_dict()
    new_dict["prompt"] = "total replacement"
    branch_dict = set_dict_from_path(branch_dict, new_dict, [])
    assert branch_dict["prompt"] == "total replacement"
    assert len(branch_dict["branch"]) == 0
    # Test setting a dict with invalid parameters
    new_dict = set_dict_from_path(branch_dict, {}, [0, 3, 4])
    assert new_dict["prompt"] == "total replacement"
    assert len(new_dict["branch"]) == 0
    new_dict = set_dict_from_path(branch_dict, {}, None)
    assert new_dict["prompt"] == "total replacement"
    assert len(new_dict["branch"]) == 0
    assert set_dict_from_path(branch_dict, None, []) is None
    assert set_dict_from_path(None, {}, []) == {}
    assert set_dict_from_path(None, {}, [1]) is None

def test_get_dict_print():
    """
    Tests the get_dict_print function.
    """
    # Create branch dict for testing
    branch_dict = get_empty_branch_dict()
    branch_dict["prompt"] = "First"
    branch_dict = add_item_to_dict(branch_dict, "s", "2-2")
    branch_dict = add_item_to_dict(branch_dict, "m", "Text!")
    branch_dict = add_item_to_dict(branch_dict, "y", "Other")
    branch_dict = create_branch_in_dict(branch_dict, "Question?", ["Yes", "No", "Maybe"])
    new_dict = get_empty_branch_dict()
    new_dict["prompt"] = "Question?"
    new_dict["response"] = "No"
    new_dict = add_item_to_dict(new_dict, "s", "2-3")
    new_dict = add_item_to_dict(new_dict, "m", "Thing")
    new_dict = create_branch_in_dict(new_dict, "New Prompt!", ["Other", "Response"])
    branch_dict = set_dict_from_path(branch_dict, new_dict, [1])
    end_dict = get_dict_from_path(branch_dict, [1,1])
    end_dict = add_item_to_dict(end_dict, "m", "Item")
    end_dict["end"] = True
    branch_dict = set_dict_from_path(branch_dict, end_dict, [1,1])
    # Test getting print with previous save and next responses
    response = get_dict_print(branch_dict, [1])
    text = "(...)\n"\
                +"\033[36m(S) 2-2\033[0m\n"\
                +"\033[31m(P) Question?\033[0m\n"\
                + "\033[32m    ﹂No\033[0m\n"\
                + "     \033[36m(S) 2-3\033[0m\n"\
                + "     \033[35m(E) Thing\033[0m\033[31m\n"\
                + "     (P) New Prompt!\033[0m\033[32m\n"\
                + "         ﹂Other\033[0m\033[32m\n"\
                + "         ﹂Response\033[0m"
    assert response == text
    # Test getting print with no previous save
    response = get_dict_print(branch_dict, [])
    text = "\033[36m(S) 2-2\033[0m\n"\
                + "\033[35m(E) Text!\033[0m\n"\
                + "\033[93m(E) Other\033[0m\033[31m\n"\
                + "(P) Question?\033[0m\033[32m\n"\
                + "    ﹂Yes\033[0m\033[32m\n"\
                + "    ﹂No\033[0m\033[32m\n"\
                + "    ﹂Maybe\033[0m"
    assert response == text
    # Test getting print with no item list or responses
    response = get_dict_print(branch_dict, [1,0])
    text = "(...)\n"\
                + "\033[36m(S) 2-3\033[0m\n"\
                + "\033[31m(P) New Prompt!\033[0m\n"\
                + "\033[32m    ﹂Other\033[0m"
    assert response == text
    # Test getting print for branch marked as end
    response = get_dict_print(branch_dict, [1,1])
    text = "(...)\n"\
                + "\033[32m[COMPLETE BRANCH]\033[0m\n"\
                + "\033[36m(S) 2-3\033[0m\n"\
                + "\033[31m(P) New Prompt!\033[0m\n"\
                + "\033[32m    ﹂Response\033[0m\n"\
                + "     \033[35m(E) Item\033[0m\n"\
                + "     [END]"
    assert response == text
    # Test getting print with invalid paramaters
    assert get_dict_print(branch_dict, [1,1,1]) == ""
    assert get_dict_print({}, []) == ""
    assert get_dict_print(None, []) == ""

def test_read_write_branch_dict():
    """
    Tests the read_write_branch_dict function.
    """
    # Test reading and writing a branch dict
    test_dir = get_test_dir()
    start = get_empty_branch_dict()
    start = add_item_to_dict(start, "r", "Thing")
    start = create_branch_in_dict(start, "Question?", ["Sure", "No."])
    file = join(test_dir, "branch.json")
    write_branch_dict(join(test_dir, "branch.json"), start)
    start = None
    assert exists(file)
    read = read_branch_dict(file)
    assert read["prompt"] is None
    assert read["response"] is None
    assert len(read["item_list"]) == 1
    assert read["item_list"][0]["text"] == "Thing"
    assert len(read["branch"]) == 2
    assert read["branch"][0]["prompt"] == "Question?"
    assert not read["branch"][0]["end"]
    assert read["branch"][0]["response"] == "Sure"
    assert read["branch"][1]["response"] == "No."
    # Test reading JSONs that aren't a branch dict
    json = get_empty_branch_dict()
    json["prompt"] = False
    file = abspath(join(test_dir, "not_branch.json"))
    with open(abspath(file), "w") as out_file:
        dump(json, out_file, indent=4, separators=(",", ": "))
    assert read_branch_dict(file) is None
    json = {"prompt":"thing", "thing":"other"}
    with open(abspath(file), "w") as out_file:
        dump(json, out_file, indent=4, separators=(",", ": "))
    assert read_branch_dict(file) is None
    json = {"not":"branch", "thing":"other"}
    with open(abspath(file), "w") as out_file:
        dump(json, out_file, indent=4, separators=(",", ": "))
    assert read_branch_dict(file) is None
    # Test reading an invalid file
    assert read_branch_dict(None) is None
    assert read_branch_dict("/non/existist/file.json") is None
    # Test writing invalid branch and invalid file
    write_branch_dict(None, read)
    write_branch_dict("/non/existant/dir/thing/blah.json", read)
    file = join(test_dir, "cant.json")
    write_branch_dict(file, None)
    assert not exists(file)

def test_is_complete():
    """
    Tests the is_complete function.
    """
    # Test whether a simple branch is complete
    start = get_empty_branch_dict()
    assert not is_complete(start)
    start["end"] = True
    assert is_complete(start)
    # Test getting whether a branch dict with multiple branches is complete
    start = create_branch_in_dict(start, "'Tis a Question", ["Yes", "No", "Maybe"])
    assert not is_complete(start)
    branch = get_dict_from_path(start, [0])
    branch["end"] = True
    start = set_dict_from_path(start, branch, [0])
    assert not is_complete(start)
    branch = get_dict_from_path(start, [1])
    branch["end"] = True
    start = set_dict_from_path(start, branch, [1])
    assert not is_complete(start)
    branch = get_dict_from_path(start, [2])
    branch["end"] = True
    start = set_dict_from_path(start, branch, [2])
    assert is_complete(start)
    # Test that sub branches are complete
    branch = get_dict_from_path(start, [1])
    branch = create_branch_in_dict(branch, "Another Fork", ["Yep", "No"])
    start = set_dict_from_path(start, branch, [1])
    assert not is_complete(start)
    assert is_complete(get_dict_from_path(start, [2]))
    branch = get_dict_from_path(start, [1, 0])
    branch["end"] = True
    start = set_dict_from_path(start, branch, [1, 0])
    assert not is_complete(start)
    branch = get_dict_from_path(start, [1, 1])
    branch["end"] = True
    start = set_dict_from_path(start, branch, [1, 1])
    assert is_complete(start)
    # Test using invalid parameters
    assert not is_complete({})
    assert not is_complete(None)
