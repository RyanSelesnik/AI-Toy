from . import math_game_utils
import os


def test_converts_arr_of_strs_to_ints():
    entities = ['one', 'two', 'three']
    assert [1, 2, 3] == math_game_utils.map_entities_to_ints(entities)


def test_case_insensitive():
    entities = ['ONE', 'TWO', 'three']
    assert [1, 2, 3] == math_game_utils.map_entities_to_ints(entities)


def test_order_is_preserved():
    """Tests that order is preserved under the mapping"""
    entities = ['five', 'three', 'seven']
    assert [5, 3, 7] == math_game_utils.map_entities_to_ints(entities)


def test_initial_call_to_validate_list():

    valid_list = [1, 2, 3]

    path_to_number_file = './latest_number.txt '
    os.system(f"touch {path_to_number_file}")
    # Ensure file is empty
    open(path_to_number_file, 'w').close()
    assert math_game_utils.list_is_valid(valid_list, path_to_number_file)


def test_multiple_calls_to_validate_list():
    """Tests multiple calls to list_is_valid()"""
    path_to_number_file = './latest_number.txt '
    os.system(f"touch {path_to_number_file}")
    first_valid_list = [1, 2, 3]
    math_game_utils.list_is_valid(first_valid_list, path_to_number_file)
    second_valid_list = [4, 5, 6]
    assert math_game_utils.list_is_valid(
        second_valid_list, path_to_number_file)

    third_invalid_list = [8, 9]

    assert math_game_utils.list_is_valid(
        third_invalid_list, path_to_number_file) == False


def test_empty_list_is_invalid():
    pass


# def test_list_is_valid_called_twice():
#     """Tests two calls to list_is_valid()"""
#     first_valid_list = [1, 2, 3]
#     math_game_utils.list_is_valid(first_valid_list)
#     second_valid_list = [4, 5, 6]
#     assert math_game_utils.list_is_valid(second_valid_list)


# def test_invalid_list():
#     """Tests two calls to list_is_valid(), when the second call contains an anvalid list"""
#     first_valid_list = [1, 2, 3]
#     math_game_utils.list_is_valid(first_valid_list)
#     second_invalid_list = [5, 6, 7]
#     assert math_game_utils.list_is_valid(second_invalid_list) == False
