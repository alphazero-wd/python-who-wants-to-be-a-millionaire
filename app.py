from enum import Enum
from math import ceil
import os
from dotenv import load_dotenv
import requests
import random
import html
from typing import Dict, List
from openai import OpenAI

load_dotenv()

NUMBER_OF_QUESTIONS = 15
GENERAL_KNOWLEDGE_CATEGORY_CODE = 9
CHECKPOINTS_COUNT = NUMBER_OF_QUESTIONS // 3


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

  def get_option(self, option_name: str):
    option_index = self.choices.index(option_name)
    return f'{self.__map_index_to_option(option_index)}. {self.choices[option_index]}'

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

  @staticmethod
  def map_difficulty_scale(difficulty):
    match difficulty:
      case 1: return 'easy'
      case 2: return 'medium'
      case 3: return 'hard'

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

  def __str__(self) -> str:
    options = [self.get_option(option) for option in self.choices]
    formatted_options_str = '\n'.join(options)
    return f"{self.__name}\n{formatted_options_str}"

  def compare_answers(self, option: str):
    option_index = self.map_option_to_index(option.upper())
    return option_index == self.choices.index(self.correct_answer)

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
  def correct_answer(self):
    return self.__correct_answer


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
    self.__choices[Choice.HELP.value] = 'Ask AI for help'

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

  def enable_help(self):
    del self.__choices[Choice.HELP.value]

  def display_choices(self):
    print('You have the following choices:')
    for key, value in self.__choices.items():
      print(f'[{key}/{key.lower()}]: {value}')

  def validate_player_choice(self, choice: str):
    return choice.upper() in self.__choices


class BotAssistant:
  __client: OpenAI

  def __init__(self):
    self.__client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

  def assist(self, prompt: str):
    Message.display_help_response_message()
    stream = self.__client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant for a contestant in a \"Who Wants to be a Millionaire\" game. Your job is to provide hints about the answer to the question the contestant is asking. However, you can possibly deceive the contestant by providing wrong hints to make them lose the game."},
            {"role": "user", "content": prompt}
        ], stream=True)
    for chunk in stream:
      if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")


class Prize:
  __prizes = 0, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000

  @staticmethod
  def earn(question_number):
    return Prize.__format_money(Prize.__prizes[question_number])

  @staticmethod
  def __format_money(money: int):
    return f'${money:,}'


class API:
  __http: requests

  def __init__(self, http):
    self.__http = http

  def fetch(self, url):
    res = self.__http.get(url)
    return res.json()


class QuestionsManager:
  __questions_answered: int
  __questions: List[Question]
  __api: API

  def __init__(self, api):
    self.__questions_answered = 0
    self.__questions: List[Question] = []
    self.__api = api

  def fetch_questions(self, difficulty: str = 'easy'):
    url = f'https://opentdb.com/api.php?category={GENERAL_KNOWLEDGE_CATEGORY_CODE}&type=multiple&amount={CHECKPOINTS_COUNT}&difficulty={difficulty}'
    response = self.__api.fetch(url)
    self.__load_questions(response['results'])

  @property
  def __questions_left_to_checkpoint(self):
    return CHECKPOINTS_COUNT - (self.questions_answered % CHECKPOINTS_COUNT)

  @property
  def is_checkpoint(self):
    return self.questions_answered > 0 and self.__questions_left_to_checkpoint == 0

  @property
  def near_checkpoint(self):
    return self.__questions_left_to_checkpoint == 1

  @property
  def questions_answered(self):
    return self.__questions_answered

  @property
  def next_difficulty_level(self):
    return ceil(self.questions_answered // CHECKPOINTS_COUNT) + 1

  @property
  def deck(self):
    return self.__questions

  def move_to_next_question(self):
    self.__questions_answered += 1

  def __load_questions(self, questions: List[Dict[str, str]]):
    self.__questions.extend(
      [Question(
        question['question'],
        question['difficulty'],
        question['correct_answer'],
        question['incorrect_answers']
      ) for question in questions]
    )


class Player:
  __help_available: bool
  __choices_manager: ChoicesManager
  __questions_manager: QuestionsManager
  __bot_assistant: BotAssistant

  def __init__(self, choices_manager, questions_manager, bot_assistant):
    self.__choices_manager = choices_manager
    self.__questions_manager = questions_manager
    self.__bot_assistant = bot_assistant

  @property
  def choices_manager(self):
    return self.__choices_manager

  @property
  def questions_manager(self):
    return self.__questions_manager

  @property
  def is_millionaire(self):
    return self.questions_manager.questions_answered == NUMBER_OF_QUESTIONS

  def input_choice(self):
    choice = input('Enter your choice: ')
    while not self.choices_manager.validate_player_choice(choice):
      choice = input('Invalid choice. Please enter one of the above option: ')
    return choice

  def leave_game(self):
    exit()

  def enable_fifty_fifty(self):
    self.choices_manager.enable_fifty_fifty()

  @property
  def check_help(self):
    return self.__help_available

  def enable_help(self, question: Question):
    self.__help_available = False
    self.__bot_assistant.assist(str(question))
    self.choices_manager.enable_fifty_fifty()


class ChoiceHandler:
  __player: Player

  def __init__(self, player):
    self.__player = player

  def handle_choice(self, choice: str, question: Question, question_number: int):
    match choice.upper():
      case Choice.HELP.value:
        self.__handle_help_choice(question, question_number)
      case Choice.QUIT.value:
        self.__handle_quit_choice(question_number)
      case Choice.FIFTY_FIFTY.value:
        self.__handle_fifty_fifty_choice(question, question_number)
        self.__redisplay_question(question, question_number)
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

  def __handle_help_choice(self, question: Question, question_number):
    self.__player.enable_help(question)
    self.__redisplay_question(question, question_number)

  def __handle_quit_choice(self, question_number: int):
    Message.display_quit_message(question_number)
    self.__player.leave_game()

  def __handle_fifty_fifty_choice(self, question: Question, question_number: int):
    self.__player.enable_fifty_fifty()
    question.eliminate_two_wrong_choices()
    self.__redisplay_question(question, question_number)

  def __redisplay_question(self, question: Question, question_number: int):
    question.display(question_number + 1)
    self.__player.choices_manager.display_choices()
    choice = self.__player.input_choice()
    self.handle_choice(choice, question, question_number)

  def __handle_player_answer(self, choice: str, question: Question, question_number: int):
    if not question.compare_answers(choice):
      Message.display_incorrect_message(question, question_number)
      self.__player.leave_game()
    else:
      Message.display_correct_message(question_number)
      self.__player.questions_manager.move_to_next_question()
      if self.__player.is_millionaire:
        Message.display_millionaire_message()
        self.__player.leave_game()


class Message:
  @staticmethod
  def display_intro():
    print('Welcome to Who Wants to be a Millionaire.')
    print('To win the game, you have to overcome 15 QUESTIONS in INCREASING DIFFICULTIES.')
    print('You will EARN AN AMOUNT OF MONEY as you answer a question correctly.')
    print('You will also LOSE AN AMOUNT OF MONEY and LEAVE THE GAME if you get 1 question WRONG.')
    print('If you get stuck on 1 question, you can enable 50:50 IN THAT QUESTION ONLY, which will OMIT 2 WRONG ANSWERS for you.')
    print('If you have used 50:50 and you are uncertain of an answer for a particular question, you can also choose to LEAVE THE GAME to preserve the money you have earned.')
    print('If you answer all 15 questions correctly by typing your answer, you are a "millionaire".')

  @staticmethod
  def display_checkpoint_message(difficulty: str):
    print('--------')
    if difficulty == 'medium':
      print('Easy right?', end=' ')
    elif difficulty == 'hard':
      print('Not challenging enough?', end=' ')
    print('Now, we shall level up the difficulty to ' + difficulty)
    print('--------')
    print('\n')

  @staticmethod
  def display_loading():
    print("Loading questions... 🌀")

  @staticmethod
  def display_game_started():
    print("Questions loaded. Get ready 🏁")
    print('We shall get started with a few easy questions.\n')

  @staticmethod
  def display_fifty_fifty_message():
    print('50:50 enabled. Two wrong answers have been eliminated')

  @staticmethod
  def display_help_response_message():
    print('🤖 AI is responding...')

  @staticmethod
  def display_correct_message(question_number: int):
    print(f"Correct! Your current prize is {Prize.earn(question_number + 1)}")

  @staticmethod
  def display_millionaire_message():
    print("You've finally conquered the \"millionaire\" title. Congrats!")

  @staticmethod
  def display_incorrect_message(question: Question, question_number: int):
    print('Oops, it seems your answer is incorrect :(')
    print(
      f'The correct answer is {question.get_option(question.correct_answer)}')
    print(
      f'You have left the game with {Prize.earn(question_number - (question_number % CHECKPOINTS_COUNT))}')

  @staticmethod
  def display_goodbye():
    print("Thanks for joining in the game. Have a nice day :)")

  @staticmethod
  def display_quit_message(question_number: int):
    message = f"You've decided to leave the game with {Prize.earn(question_number)}. Have a nice day :)"
    print(message)


class Game:
  __player: Player
  __choice_handler: ChoiceHandler

  def __init__(self, player, choice_handler):
    self.__player = player
    self.__choice_handler = choice_handler

  def __play(self):
    for i, question in enumerate(self.__player.questions_manager.deck):
      difficulty = Question.map_difficulty_scale(
        self.__player.questions_manager.next_difficulty_level)
      if self.__player.questions_manager.near_checkpoint:
        self.__fetch_harder_questions(difficulty)
      if self.__player.questions_manager.is_checkpoint:
        self.__handle_checkpoint(difficulty)
      question.display(i + 1)
      self.__player.choices_manager.display_choices()
      choice = self.__player.input_choice()
      self.__choice_handler.handle_choice(choice, question, i)
      self.__player.choices_manager.reset()

  def __fetch_harder_questions(self, difficulty: str):
    self.__player.questions_manager.fetch_questions(difficulty)

  def __handle_checkpoint(self, difficulty: str):
    Message.display_checkpoint_message(difficulty)

  @staticmethod
  def __ask_to_start():
    message = 'Are you ready to play? Press Y to play, or press other keys to exit: '
    to_start = input(message)
    return to_start.lower().strip() in ('yes', 'y')

  def start(self):
    Message.display_intro()
    if self.__ask_to_start():
      Message.display_loading()
      self.__player.questions_manager.fetch_questions()
      Message.display_game_started()
      self.__play()
    else:
      Message.display_goodbye()
      self.__player.leave_game()


if __name__ == '__main__':
  api = API(requests)
  player = Player(ChoicesManager(), QuestionsManager(api), BotAssistant())
  choice_handler = ChoiceHandler(player)
  game = Game(player, choice_handler)
  game.start()
