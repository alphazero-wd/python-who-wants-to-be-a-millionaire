import requests
import random
import html
from typing import List
from colorama import Fore


class Question:
  def __init__(self, question, category, type, difficulty, correct_answer, incorrect_answers):
    self.question = question
    self.category = category
    self.type = type
    self.difficulty = difficulty
    self.correct_ans = correct_answer
    self.choices = [correct_answer, *incorrect_answers]
    self.choices.sort(key=lambda _: 0.5 - random.random())


class Game:
  def __init__(self):
    self.questions: List[Question] = []
    self.bounty = 0
    self.qs_rewards = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]

  def map_difficulty(self, difficulty):
    if difficulty == 'easy':
      difficulty = 1
    elif difficulty == 'medium':
      difficulty = 2
    if difficulty == 'hard':
      difficulty = 3
    return difficulty

  def display_current_money(self):
    print("Total prize: ${:,}".format(self.bounty))


  def fetch_api(self):
    URL = 'https://opentdb.com/api.php?&amount=15'
    res = requests.get(URL)
    results = res.json()['results']
    for question in results:
      self.questions.append(
          Question(
            question['question'],
            question['category'],
            question['type'],
            question['difficulty'],
            question['correct_answer'],
            question['incorrect_answers']
          ))
    self.questions.sort(key=lambda x: self.map_difficulty(x.difficulty))

  def start(self):
    self.fetch_api()
    print('Welcome to Who Wants to be a Millionaire.')
    print('To win the game, you have to overcome 15 questions.')
    print('You will earn an amount of money as you answer a question correctly.')
    isConfirmed = input('If you answer all 15 questions correctly by typing your answer, you are a "millionaire". Are you ready to play? [y/n]: ')
    if isConfirmed.lower() in ['yes', 'y']:
      self.display_questions()
    else: exit()

  def display_questions(self):
    for i, question in enumerate(self.questions):
      print(f'\nQuestion {i + 1} ({question.difficulty}, {question.category}): {html.unescape(question.question)}\n----------')
      player_choices = ['A', 'B', 'C', 'D', 'Q']
      if question.type == 'boolean': player_choices = ['A', 'B', 'Q']
      for j, choice in enumerate(question.choices):
        print(f'{player_choices[j]}. {html.unescape(choice)}')
      instructions_on_type = '/'.join(player_choices[:(4 if question.type == 'multiple' else 2)] )
      player_choice = input(f'Choose the answer [{instructions_on_type}] or press Q to leave the game: ').upper()

      while player_choice not in player_choices:
        player_choice = input('That\'s not a valid choice. Please choose the answer [A/B/C/D] or press Q to leave the game: ').upper()

      if player_choice == 'Q':
        print('It\'s a safe choice to leave the game if you\'re uncertain of your answer. Good choice :)')
        self.display_current_money()
        break

      player_choice_index = player_choices.index(player_choice)
      if question.choices[player_choice_index] == question.correct_ans:
        self.bounty = self.qs_rewards[i]
        if i == len(self.questions) - 1:
          print('You\'ve become a millionaire. Good luck with your life :)')
          self.display_current_money()
          break
        print('\nYou are correct. Let\'s move on to the next question.')
        self.display_current_money()
      else:
        if self.bounty > 1000: self.bounty = self.qs_rewards[i - (i % 5) - 1]
        print(f'Oops, the correct answer is {player_choices[question.choices.index(question.correct_ans)]}. {question.correct_ans} :(')
        self.display_current_money()
        break

game = Game()
game.start()
