#!/usr/bin/env python3

from argparse import ArgumentParser
from os import pardir, system
from os import name as os_name
from os.path import abspath, basename, join, exists
from typing import List
from vn_organizer.main.vn_organizer import add_item_to_dict
from vn_organizer.main.vn_organizer import create_branch_in_dict
from vn_organizer.main.vn_organizer import get_dict_print
from vn_organizer.main.vn_organizer import get_dict_from_path
from vn_organizer.main.vn_organizer import get_empty_branch_dict
from vn_organizer.main.vn_organizer import read_branch_dict
from vn_organizer.main.vn_organizer import set_dict_from_path
from vn_organizer.main.vn_organizer import write_branch_dict

def user_edit(file:str=None, branch_dict:dict=None):
    path = []
    text = None
    cur_dict = branch_dict
    while True:
        # Clear the terminal
        if os_name == "nt":
            system("cls")
        else:
            system("clear")
        # Print the branch dict at the current path
        print(get_dict_print(cur_dict, path))
        # Print additional text if present
        if text is not None:
            print(f"\n{text}")
        # Get user command
        print()
        response = input("Command (h for help): ").lower()
        # Check user command
        if response == "w":
            # Write dict to file
            write_branch_dict(file, cur_dict)
            text = "Saved File"
            continue
        if response == "a":
            # Add element to the dict
            cur_dict = add_element(cur_dict, path)
            text = None
            continue
        if response == "d":
            # Delete element from the dict
            cur_dict = delete_element(cur_dict, path)
            text = None
            continue
        if response == "m":
            # Move into part of the dict
            path = move(cur_dict, path)
            text = None
            continue
        if response == "f":
            # Toggle the end flag for branch of the dict
            sub_dict = get_dict_from_path(cur_dict, path)
            sub_dict["end"] = not sub_dict["end"]
            if len(sub_dict["branch"]) > 0:
                sub_dict["end"] = False
            cur_dict = set_dict_from_path(cur_dict, sub_dict, path)
            text = "Toggled END"
            continue
        if response == "q":
            break
        # Print help command
        text = "Commands:\n"\
                    + "h - help\n"\
                    + "a - add element\n"\
                    + "d - delete element\n"\
                    + "m - move\n"\
                    + "f - toggle whether the branch ends"\
                    + "w - write to file\n"\
                    + "q - quit program (without saving)"
                    
    return False

def move(branch_dict:dict=None, path:List[int]=None) -> List[int]:
    # Print list of paths to move down
    cur_dict = get_dict_from_path(branch_dict, path)
    print()
    size = len(cur_dict["branch"])
    for i in range(0, size):
        print("(" + str(i+1) + ") " + cur_dict["branch"][i]["response"])
    # Get user input
    try:
        print()
        response = int(input("Which Path? (0 to move up): ")) - 1
        if response == -1:
            return path[:-1]
        if response < -1 or response > size-1:
            return path
        new_path = path
        new_path.append(response)
        return new_path
    except ValueError:
        return path

def delete_element(branch_dict:dict=None, path:List[int]=None) -> dict:
    # Get user input for what kind of element to add
    full_dict = branch_dict
    cur_dict = get_dict_from_path(full_dict, path)
    response = input("Delete (e - event, b - branch): ")
    if response == "e":
        # Remove one of the events from the item list
        item_list = cur_dict["item_list"]
        for i in range(0, len(item_list)):
            print("(" + str(i+1) + ") " + item_list[i]["text"])
        try:
            index = int(input("Delete: ")) - 1
            if index < 0:
                return full_dict
            del item_list[index]
            cur_dict["item_list"] = item_list
        except (IndexError, ValueError):
            return full_dict
    elif response == "b":
        # Remove one of the branches
        branches = cur_dict["branch"]
        for i in range(0, len(branches)):
            print("(" + str(i+1) + ") " + branches[i]["response"])
        try:
            index = int(input("Delete: ")) - 1
            if index < 0 or index > len(branches)-1:
                return full_dict
            if input("Delete response and all sub branches? (Y/N)").lower() == "y":
                del branches[index]
            cur_dict["branch"] = branches
        except ValueError:
            return full_dict
    # Replace the section of the dict
    full_dict = set_dict_from_path(full_dict, cur_dict, path)
    # Return the dict
    return full_dict

def add_element(branch_dict:dict=None, path:List[int]=None) -> dict:
    # Get user input for element to add
    full_dict = branch_dict
    cur_dict = get_dict_from_path(full_dict, path)
    response = input("Add (s - save, e - event, b - branch): ").lower()
    # Check the input
    if response == "s":
        # Create a save element
        save = input("Save Name: ")
        cur_dict = add_item_to_dict(cur_dict, "s", save)
    elif response == "e":
        # Create event
        event = input("Event Name: ")
        color = input("Color (R, G, B, C, Y, M, W): ").lower()
        cur_dict = add_item_to_dict(cur_dict, color, event)
    elif response == "b":
        # Create branches
        responses = []
        prompt = input("Branch Prompt: ")
        while True:
            r = input("Branch Response (q to stop): ")
            if r.lower() == "q":
                break
            responses.append(r)
        cur_dict = create_branch_in_dict(cur_dict, prompt, responses)
    # Replace the section of the dict
    full_dict = set_dict_from_path(full_dict, cur_dict, path)
    # Return the dict
    return full_dict

def main():
    # Get filename from the user
    parser = ArgumentParser()
    parser.add_argument(
            "file",
            help="JSON file with branch info.",
            type=str)
    args = parser.parse_args()
    full_file = abspath(args.file)
    # Check if directory of the file exists
    if not exists(abspath(join(full_file, pardir))):
        print("Directory doesn't exist.")
        return False
    # Check if given file exists
    if not exists(full_file):
        print("File doesn't exist.")
        response = input(f"Create file {basename(full_file)}? (Y/N): ").lower()
        if not response == "y":
            return False
        # Create file is specified
        new_dict = get_empty_branch_dict()
        write_branch_dict(full_file, new_dict)
    # Read the given file
    branch_dict = read_branch_dict(full_file)
    # Check if the file is a proper branch dict
    if branch_dict is None:
        print("File is not correctly formatted.")
        return False
    # Start the user editing process
    user_edit(full_file, branch_dict)

if __name__ == "__main__":
    main()
