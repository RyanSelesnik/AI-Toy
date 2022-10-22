from . import memory_game_utils
from rasa_sdk.executor import CollectingDispatcher

def test_is_valid_cond_1():
    user_turn = ['vegetables']
    bot_prev_turn = []
    dispatcher=CollectingDispatcher()
    assert True == memory_game_utils.isValid(bot_prev_turn, user_turn, dispatcher)

def test_is_valid_cond_2():
    user_turn = ['vegetables','fruit', 'pets']
    bot_prev_turn = ['vegetables', 'clothes']
    dispatcher = CollectingDispatcher()
    assert False == memory_game_utils.isValid(bot_prev_turn, user_turn, dispatcher)

# def test_is_valid_cond_2_variation():
#     user_turn = ['vegetables']
#     bot_prev_turn = ['vegetables', 'clothes']
#     dispatcher = CollectingDispatcher()
#     assert False == memory_game_utils.isValid(bot_prev_turn, user_turn, dispatcher)
    
def test_is_valid_cond_3():
    user_turn = ['vegetables','fruit', 'pets']
    bot_prev_turn = ['vegetables', 'fruit']
    dispatcher = CollectingDispatcher()
    assert True == memory_game_utils.isValid(bot_prev_turn, user_turn, dispatcher)

def test_is_valid_cond_2_var_2():
    user_turn = ['pie', 'crumpets', 'doll', 'sugar', 'pillow', 'eggplant']
    bot_prev_turn = ['pie', 'crumpets', 'doll', 'sugar','flowers', 'pillow']
    dispatcher = CollectingDispatcher()
    assert False == memory_game_utils.isValid(bot_prev_turn, user_turn, dispatcher)

def test_computer_addition_return():
    user_turn = ['vegetables','fruit', 'pets']
    computer_addition = memory_game_utils.computer_turn(user_turn)
    assert type(computer_addition) is str

def test_computer_choice_in_file():
    user_turn=['vegetables','fruit', 'pets']
    computer_choice = memory_game_utils.computer_turn(user_turn)
    with open('data/memory_game/items.txt', 'r') as file:
        list = file.read()
    assert computer_choice in list

def test_new_bot_turn():
    user_turn=['vegetables', 'fruit', 'clothes', 'animals']
    bot_turn = memory_game_utils.proceedValidTurn(user_turn)
    assert bot_turn[:-1] == user_turn

