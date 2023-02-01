import requests
import random
import html
from typing import List


class Question:
  def __init__(self, question, difficulty, correct_answer, incorrect_answers):
    self.question = question
    self.difficulty = difficulty
    self.correct_ans = correct_answer
    self.choices = [correct_answer, *incorrect_answers]
    self.incorrect_answers = incorrect_answers
    self.choices.sort(key=lambda _: 0.5 - random.random())


class Game:
  def __init__(self):
    self.questions: List[Question] = []
    self.bounty = 0
    self.qs_rewards = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
    self.player_choices = ['A', 'B', 'C', 'D', 'Q', 'H']
    self.fifty_fifty_available = True

  def map_difficulty(self, difficulty):
    if difficulty == 'easy':
      difficulty = 1
    elif difficulty == 'medium':
      difficulty = 2
    if difficulty == 'hard':
      difficulty = 3
    return difficulty

  def display_current_money(self):
    return "${:,}".format(self.bounty)

  def fetch_api(self):
    """
      Visit the documentation for the API [here](https://opentdb.com/api_config.php)
    """
    for difficulty in ['easy', 'medium', 'hard']:
      URL = 'https://opentdb.com/api.php?category=9&type=multiple&amount=5&difficulty=' + difficulty
      res = requests.get(URL)
      results = res.json()['results']
      for question in results:
        self.questions.append(
            Question(
              question['question'],
              question['difficulty'],
              question['correct_answer'],
              question['incorrect_answers']
            ))

    self.questions.sort(key=lambda x: self.map_difficulty(x.difficulty))

  def enable_fifty_fifty(self, question: Question):
    # find another arbitrary incorrect answer
    random_incorrect_ans = random.choice(question.incorrect_answers)

    # map the 50:50 version
    self.player_choices = ['A', 'B', 'Q', 'H']
    question.choices = [question.correct_ans, random_incorrect_ans]
    question.choices.sort(key=lambda _: .5 - random.random())

    print('\nTwo wrong answers have been omitted\n-----------')
    for i, choice in enumerate(question.choices):
      print(f'{self.player_choices[i]}. {choice}')
    self.fifty_fifty_available = False


  def start(self):
    self.fetch_api()
    print('Welcome to Who Wants to be a Millionaire.')
    print('To win the game, you have to overcome 15 QUESTIONS in INCREASING DIFFICULTIES.')
    print('You will EARN AN AMOUNT OF MONEY as you answer a question correctly.')
    print('You will also LOSE AN AMOUNT OF MONEY and LEAVE THE GAME if you get 1 question WRONG.')
    print('If you get stuck on 1 question, you can enable 50:50 IN THAT QUESTION ONLY, which will OMIT 2 WRONG ANSWERS for you.')
    print('If you have used 50:50 and you are uncertain of an answer for a particular question, you can also choose to LEAVE THE GAME to preserve the money you have earned.')
    print('If you answer all 15 questions correctly by typing your answer, you are a "millionaire".')
    isConfirmed = input('Are you ready to play? Press Y to play, press N to exit: ').lower().strip()
    if isConfirmed in ['yes', 'y']:
      self.display_questions()
    else: exit()

  def receive_user_choice(self):
    fifty_fifty_prompt = ' or press H to enable 50:50' if self.fifty_fifty_available else ''
    player_choice = input(f'Choose the answer [A/B/C/D] or press Q to leave the game{fifty_fifty_prompt}: ').upper().strip()

    while player_choice == 'H' and not self.fifty_fifty_available:
      print('\nYou have used 50:50 already so you cannot use it any more.')
      player_choice = input(f'Please choose the answer [A/B/C/D] or press Q to leave the game: ').upper().strip()

    while player_choice not in self.player_choices:
      player_choice = input(f'\nThat is not a valid choice! Please choose the answer [A/B/C/D] or press Q to leave the game: ').upper().strip()
    return player_choice

  def display_questions(self):
    for i, question in enumerate(self.questions):
      print(f'\nQuestion {i + 1} ({question.difficulty}): {html.unescape(question.question)}\n----------')

      self.player_choices = ['A', 'B', 'C', 'D', 'Q', 'H']

      for j, choice in enumerate(question.choices):
        print(f'{self.player_choices[j]}. {html.unescape(choice)}')

      player_choice = self.receive_user_choice()

      if player_choice == 'Q':
        print('It\'s a safe choice to leave the game if you\'re uncertain of your answer. Good choice :)')
        print(f'Total prize: {self.display_current_money()}')
        break

      if player_choice == 'H' and self.fifty_fifty_available:
        self.enable_fifty_fifty(question)
        player_choice = self.receive_user_choice()

      player_choice_index = self.player_choices.index(player_choice)

      if question.choices[player_choice_index] == question.correct_ans:
        self.bounty = self.qs_rewards[i]
        if i == len(self.questions) - 1:
          print('You\'ve become a MILLIONAIRE. Good luck with your life :)')
          break
        print('\nYou are correct. Let\'s move on to the next question.')
        print(f'Money won: {self.display_current_money()}')

      else:
        if self.bounty > 1000: self.bounty = self.qs_rewards[i - (i % 5) - 1]
        print(f'Oops, the correct answer is {self.player_choices[question.choices.index(question.correct_ans)]}. {question.correct_ans}')
        print('Good luck next time :(')
        print(f'Total prize: {self.display_current_money()}')
        break

game = Game()
game.start()
