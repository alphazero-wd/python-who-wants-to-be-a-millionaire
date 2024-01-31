from enum import Enum
import requests
import random
import html
from typing import Dict, List

NUMBER_OF_QUESTIONS = 15
GENERAL_KNOWLEDGE_CATEGORY_CODE = 9


class Question:
  __name: str
  __difficulty: str
  __correct_answer: str
  __incorrect_answers: List[str]
  __choices: list[str]

  def __init__(self, name, difficulty, correct_answer, incorrect_answers):
    self.__name = name
    self.__difficulty = difficulty
    self.__correct_answer = correct_answer
    self.__incorrect_answers = incorrect_answers
    self.__shuffle_choices()

  @property
  def choices(self):
    return self.__choices

  @property
  def correct_answer(self):
    return f'{self.__map_index_to_option(self.correct_answer_position)}. {self.__correct_answer}'

  def __shuffle_choices(self):
    self.__choices = [self.__correct_answer, *self.__incorrect_answers]
    random.shuffle(self.__choices)

  def eliminate_two_wrong_choices(self):
    self.__incorrect_answers = random.choices(self.__incorrect_answers, k=1)
    self.__shuffle_choices()

  @property
  def difficulty_index(self):
    match self.__difficulty:
      case 'easy': return 1
      case 'medium': return 2
      case 'hard': return 3

  @property
  def __difficulty_emoji(self):
    match self.__difficulty:
      case 'easy': return '😀'
      case 'medium': return '🤔'
      case 'hard': return '😵'

  def __map_index_to_option(self, index: int):
    match index:
      case 0: return Choice.A.value
      case 1: return Choice.B.value
      case 2: return Choice.C.value
      case 3: return Choice.D.value
      case _: raise IndexError('Index out of bound')

  def map_option_to_index(self, option: str):
    match option.upper():
      case Choice.A.value: return 0
      case Choice.B.value: return 1
      case Choice.C.value: return 2
      case Choice.D.value: return 3
      case _: raise ValueError('Invalid Option')

  def display(self, number):
    print(
      f'\nQuestion {number} {self.__difficulty_emoji}: {html.unescape(self.__name)}\n----------')

    for i, choice in enumerate(self.__choices):
      print(f'{self.__map_index_to_option(i)}. {html.unescape(choice)}')

  @property
  def correct_answer_position(self):
    return self.__choices.index(self.__correct_answer)


class Choice(Enum):
  QUIT = 'Q'
  A = 'A'
  B = 'B'
  C = 'C'
  D = 'D'
  HELP = 'H'
  FIFTY_FIFTY = 'F'


class ChoicesManager:
  __choices: Dict[str, str]

  def __init__(self):
    self.reset()
    self.__choices[Choice.FIFTY_FIFTY.value] = 'Enable 50:50'

  def reset(self):
    self.__choices = {
      Choice.A.value: 'Select option A',
      Choice.B.value: 'Select option B',
      Choice.C.value: 'Select option C',
      Choice.D.value: 'Select option D',
      Choice.QUIT.value: 'Quit game',
    }

  @property
  def choices(self):
    return self.__choices

  def enable_fifty_fifty(self):
    del self.__choices[Choice.C.value]
    del self.__choices[Choice.D.value]
    del self.__choices[Choice.FIFTY_FIFTY.value]

  def display_choices(self):
    print('You have the following choices:')
    for key, value in self.__choices.items():
      print(f'[{key}/{key.lower()}]: {value}')

  def validate_player_choice(self, choice: str):
    return choice.upper() in self.__choices


class Player:
  __fifty_fifty_available: bool
  __choices_manager: ChoicesManager

  def __init__(self, choices_manager):
    self.__choices_manager = choices_manager
    self.__fifty_fifty_available = True

  def input_choice(self):
    choice = input('Enter your choice: ')
    while not self.__choices_manager.validate_player_choice(choice):
      choice = input('Invalid choice. Please enter one of the above option: ')
    return choice

  def leave_game(self):
    exit()

  @property
  def check_fifty_fifty(self):
    return self.__fifty_fifty_available

  def enable_fifty_fifty(self):
    self.__fifty_fifty_available = False
    self.__choices_manager.enable_fifty_fifty()


class Prize:
  __prizes = 0, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000

  @staticmethod
  def earn(question_number):
    return Prize.__format_money(Prize.__prizes[question_number])

  @staticmethod
  def __format_money(money: int):
    return f'${money:,}'


class QuestionsAPI:
  __http: requests

  def __init__(self, http):
    self.__http = http

  def fetch(self, url):
    res = self.__http.get(url)
    return res.json()


class QuestionsManager:
  __questions_answered: int
  __questions: List[Question]
  __api: QuestionsAPI

  def __init__(self):
    self.__questions_answered = 0
    self.__questions: List[Question] = []
    self.__api = QuestionsAPI(requests)

  def fetch_questions(self, difficulty: str = 'easy'):
    checkpoints = NUMBER_OF_QUESTIONS // 3
    url = f'https://opentdb.com/api.php?category={GENERAL_KNOWLEDGE_CATEGORY_CODE}&type=multiple&amount={checkpoints}&difficulty={difficulty}'
    response = self.__api.fetch(url)
    self.__load_questions(response['results'])

  @property
  def questions_answered(self):
    return self.__questions_answered

  @property
  def deck(self):
    return self.__questions

  def move_to_next_question(self):
    self.__fetch_more_difficult_questions()
    self.__questions_answered += 1

  def __fetch_more_difficult_questions(self):
    match self.__questions_answered + 1:
      case 5:
        self.fetch_questions('medium')
      case 10:
        self.fetch_questions('hard')

  def __load_questions(self, questions: List[Dict[str, str]]):
    self.__questions.extend(
      [Question(
        question['question'],
        question['difficulty'],
        question['correct_answer'],
        question['incorrect_answers']
      ) for question in questions]
    )


class ChoiceHandler:
  __player: Player
  __questions_manager: QuestionsManager
  __choices_manager: ChoicesManager

  def __init__(self, player, questions_manager, choices_manager):
    self.__player = player
    self.__questions_manager = questions_manager
    self.__choices_manager = choices_manager

  def handle_choice(self, choice: str, question: Question, question_number: int):
    match choice.upper():
      case Choice.QUIT.value:
        self.__handle_quit_choice(question_number)
      case Choice.FIFTY_FIFTY.value:
        self.__handle_fifty_fifty_choice(question, question_number)
      case Choice.A.value:
        self.__handle_player_answer(choice, question, question_number)
      case Choice.B.value:
        self.__handle_player_answer(choice, question, question_number)
      case Choice.C.value:
        self.__handle_player_answer(choice, question, question_number)
      case Choice.D.value:
        self.__handle_player_answer(choice, question, question_number)
      case _:
        raise KeyError('Invalid choice')

  def __handle_quit_choice(self, question_number: int):
    print(
      f"You've decided to leave the game with {Prize.earn(question_number)}. Have a nice day :)")
    self.__player.leave_game()

  def __handle_fifty_fifty_choice(self, question: Question, question_number: int):
    print('50:50 enabled. Two wrong answers have been eliminated')
    self.__player.enable_fifty_fifty()
    question.eliminate_two_wrong_choices()
    question.display(question_number + 1)
    self.__choices_manager.display_choices()
    choice = self.__player.input_choice()
    self.handle_choice(choice, question, question_number)

  def __handle_player_answer(self, choice: str, question: Question, question_number: int):
    if question.map_option_to_index(choice) != question.correct_answer_position:
      print('Oops, it seems your answer is incorrect :(')
      print(f'The correct answer is {question.correct_answer}')
      print(
        f'You have left the game with {Prize.earn(question_number - (question_number % 5))}')
      print("Thanks for joining in the game. Have a nice day :)")
      self.__player.leave_game()
    else:
      print(f"Correct! Your current prize is {Prize.earn(question_number + 1)}")
      if self.__questions_manager.questions_answered == NUMBER_OF_QUESTIONS:
        print("You've finally conquered the \"millionaire\" title. Congrats!")
      else:
        self.__questions_manager.move_to_next_question()


class Game:
  __questions: QuestionsManager
  __choice_handler: ChoiceHandler
  __player: Player
  __choices_manager: ChoicesManager

  def __init__(self):
    self.__choices_manager = ChoicesManager()
    self.__player = Player(self.__choices_manager)
    self.__questions = QuestionsManager()
    self.__choice_handler = ChoiceHandler(
      self.__player, self.__questions, self.__choices_manager)
    self.start()

  def __display_intro(self):
    print('Welcome to Who Wants to be a Millionaire.')
    print('To win the game, you have to overcome 15 QUESTIONS in INCREASING DIFFICULTIES.')
    print('You will EARN AN AMOUNT OF MONEY as you answer a question correctly.')
    print('You will also LOSE AN AMOUNT OF MONEY and LEAVE THE GAME if you get 1 question WRONG.')
    print('If you get stuck on 1 question, you can enable 50:50 IN THAT QUESTION ONLY, which will OMIT 2 WRONG ANSWERS for you.')
    print('If you have used 50:50 and you are uncertain of an answer for a particular question, you can also choose to LEAVE THE GAME to preserve the money you have earned.')
    print('If you answer all 15 questions correctly by typing your answer, you are a "millionaire".')

  def __play(self):
    for i, question in enumerate(self.__questions.deck):
      if i > 0 and i % 5 == 0:
        self.__remind_checkpoint('medium' if i == 5 else 'hard')
        if not self.__ask_to_start():
          self.__choice_handler.handle_choice(Choice.QUIT.value, question, i)
        print('\n')
      question.display(i + 1)
      self.__choices_manager.display_choices()
      choice = self.__player.input_choice()
      self.__choice_handler.handle_choice(choice, question, i)
      self.__choices_manager.reset()

  def __remind_checkpoint(self, difficulty: str):
    print(
      f"Congrats on reaching the {self.__questions.questions_answered}th question!")
    if difficulty == 'medium':
      print('Easy right?', end=' ')
    elif difficulty == 'hard':
      print('Not challenging enough?', end=' ')
    print('Now, we shall level up the difficulty to ' + difficulty)

  @staticmethod
  def __ask_to_start():
    message = 'Are you ready to play? Press Y to play, or press other keys to exit: '
    to_start = input(message)
    return to_start.lower().strip() in ('yes', 'y')

  def start(self):
    self.__display_intro()
    if self.__ask_to_start():
      print("Loading questions... 🌀")
      self.__questions.fetch_questions()
      print("Questions loaded. Get ready 🏁")
      print('We shall get started with a few easy questions.\n')
      self.__play()
    else:
      print('Thank you for dropping in. Have a nice day :)')
      self.__player.leave_game()


Game()
