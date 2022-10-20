
from typing import List


def map_entities_to_ints(entities) -> List[int]:
    """
    Maps a list of math game number entities into a list of integers
    TODO: Handle the case where entities = [1, 2, 3, 4]
        Args:
            entities: list of math game number entities. E.g. ['one', 'two', 'three']
        Returns: list of integers
    """
    int_lookup_dict = {"one": 1, "two": 2, "three": 3, "four": 4,
                       "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

    return [int_lookup_dict[entity.lower()] for entity in entities]


def list_is_valid(l, path_to_number_file) -> bool:
    """
    Returns True if the list is valid
    A valid list is
        1) a list of integers that contains consectutive numnber
        2) the first element in the list is succesive to the last element in the previous utterance's list
        3) the list is not empty
    """

    with open(path_to_number_file, 'r+') as f:
        prev_num = f.read()

    print(f'prev_num: {prev_num}')
    if prev_num != '':
        l.insert(0, int(prev_num))

    print(l)

    list_is_valid = (sorted(l) == list(range(min(l), max(l)+1)))
    print(list_is_valid)

    if list_is_valid and l:
        with open(path_to_number_file, 'w') as f:
            f.write(str(l[-1]))
        return True
    else:
        return False


def store_latest_number(latest_number, path_to_number_file):
    """Stores the last number in a valid number sequence uttered by the user"""
    with open(path_to_number_file, 'w') as f:
        f.write('%d' % latest_number)


if __name__ == '__main__':
    pass
