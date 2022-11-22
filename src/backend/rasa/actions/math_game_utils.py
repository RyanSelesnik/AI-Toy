
from typing import List
import os


def map_entities_to_ints(entities) -> List[int]:
    """
    Maps a list of math game number entities into a list of integers

        Args:
            entities: list of math game number entities. E.g. ['one', 'two', 'three'] or [1, 2, 3], [1, "two"]
        Returns: list of integers

        TODO: handle if unexpected inputs are entered
    """
    int_lookup_dict = {"one": 1, "two": 2, "three": 3, "four": 4,
                       "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

    try:
        list_of_ints = [int(entity) if is_int(
            entity) else int_lookup_dict[entity.lower()] for entity in entities]
    except KeyError as e:
        print(e)
        return []
    else:
        return list_of_ints


def list_is_valid(l, path_to_number_file) -> bool:
    """
    Returns True if the list is valid
    A valid list is
        1) a list of integers that contains consectutive numnber
        2) the first element in the list is succesive to the last element in the previous utterance's list
        3) the list is not empty

        Args: 
            l: a list of integers
            path_to_number_file: a path to a file
    """

    with open(path_to_number_file, 'r+') as f:
        prev_num = f.read()

    print(f'prev_num: {prev_num}')
    if prev_num != '':
        l.insert(0, int(prev_num))

    print(l)

    list_is_valid = (l == list(range(min(l), max(l)+1)))
    print(list_is_valid)

    if list_is_valid and l:
        store_latest_number(str(l[-1]), path_to_number_file)
        return True
    else:
        return False


def store_latest_number(latest_number, path_to_number_file):
    """Stores the last number in a valid number sequence uttered by the user"""
    with open(path_to_number_file, 'w') as f:
        f.write(latest_number)


def get_last_number(path_to_number_file):
    with open(path_to_number_file, 'r+') as f:
        return f.read()


def is_int(string):
    try:
        return type(int(string)) is int
    except:
        return False


def reset_game(path_to_file):
    """Resets the game by clearing the removing the text file and creating a new one"""
    try:
        os.system(f"rm {path_to_file}")
    except FileNotFoundError as e:
        print(e)

    os.system(f"touch {path_to_file}")


if __name__ == '__main__':
    pass
