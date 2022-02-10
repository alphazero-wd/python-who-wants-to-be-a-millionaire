# create questions using classes
# loop over the questions 
# if user answers correctly add bounties to them
# if they lost stop the game, and only receive a certain amount of bounty
# format the game
import random
from typing import List


class Question:
  def __init__(self, question, choices, correct_ans):
    self.question: str = question
    self.choices: List[int] = choices
    self.correct_ans: str = correct_ans
  
question_choices_keys = ['A', 'B', 'C', 'D']
valid_inputs = ['a', 'b', 'c', 'd', 'leave']
prizes = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 250000, 500000, 1000000]
questions: List[Question] = [Question('In the UK, the abbreviation NHS stands for National what Service?',  ['Humanity', 'Health', 'Honour', 'Household'], 'Health'),Question('Which Disney character famously leaves a glass slipper behind at a royal ball?',  ['Pocahontas', 'Sleeping Beauty', 'Cinderella', 'Elsa'],  'Cinderella'),Question(  'What name is given to the revolving belt machinery in an airport that delivers checked luggage from the plane to baggage reclaim?',  ['Hangar', 'Terminal', 'Concourse', 'Carousel'],  'Carousel'),Question('Which of these brands was chiefly associated with the manufacture of household locks?',  ['Phillips', 'Flymo', 'Chubb', 'Ronseal'],  'Chubb'),Question(  'The hammer and sickle is one of the most recognisable symbols of which political ideology?',  ['Republicanism', 'Communism', 'Conservatism', 'Liberalism'],  'Communism'),Question(  'Which toys have been marketed with the phrase “robots in disguise”?',  ['Bratz Dolls', 'Sylvanian Families', 'Hatchimals', 'Transformers'],  'Transformers'),Question(  'What does the word loquacious mean?',  ['Angry', 'Chatty', 'Beautiful', 'Shy'],  'Chatty'),Question(  'Obstetrics is a branch of medicine particularly concerned with what?',  ['Childbirth', 'Broken homes', 'Heart conditions', 'Old age'],  'Childbirth'),Question(  'In Doctor Who, what was the signature look of the fourth Doctor, as portrayed by Tom Baker?',  [    'Bow-tie, braces and tweed jacket',    'Wide-brimmed hat and extra long scarf',     'Pinstripe suit and trainers',     'Cape, velvet jacket and frilly shirt'  ],  'Wide-brimmed hat and extra long scarf'),Question(  'Which of these religious observances lasts for the shortest period of time during the calendar year?',  [    'Ramadan',     'Diwali',     'Lent',     'Hanukkah'  ],  'Diwali'),Question(  'At the closest point, which island group is only 50 miles south-east of the coast of Florida?',  ['Bahamas', 'US Virgin Islands', 'Turks and Caicos Islands', 'Bermuda'],  'Bahamas'),Question(  'Construction of which of these famous landmarks was completed first?',  ['Empire State Building', 'Royal Albert Hall', 'Effiel Tower', 'Big Ben Clock Tower'],  'Big Ben Clock Tower'),Question(  'Which of these cetaceans is classified as a “toothed whale”?',  ['Gray whale', 'Minke whale', 'Sperm whale', 'Humpback whale'],  'Sperm whale'),Question(  'Who is the only British politician to have held all four “Great Offices of State” at some point during their career?',  ['David Lloyd George', 'Harold Wilson', 'James Callaghan', 'John Major'],  'James Callaghan'),Question(  'In 1718, which pirate died in battle off the coast of what is now North Carolina?',  ['Calico Jack', 'Blackbeard', 'Bartholomew Roberts', 'Captain Kidd'],  'Blackbeard')]

# used to shuffle questions and choices
def shuffle(_):
  return 0.5 - random.random()

# format the money earned
def format_number(number):
  return "{:,}".format(number)

def display_money_earned(money_earned):
  return f'Money Earned: ${format_number(money_earned)}\n'

def display_questions():
    is_game_over = False
    money_earned = 0
    questions.sort(key=shuffle)
    for i, question in enumerate(questions):
      if is_game_over:
        break
      print(f'Question {i + 1}: {question.question}')
      question.choices.sort(key=shuffle)

      # loop through the choices and shuffle them
      for index, choice in enumerate(question.choices):
        print(f'{question_choices_keys[index]}. {choice}')

      # check user's choice
      player_choice = input('Type in your choice [A/B/C/D] (case-insensitive) or type in leave to leave the game: ')

      # if user leaves, preserve their prize
      if player_choice.lower() == 'leave':
        print('It\'s a safe choice to leave the game if you\'re uncertain of your answer. Good choice :)')
        print(display_money_earned(money_earned))
        is_game_over = True

      # if user enters invalid input
      while player_choice not in valid_inputs:
        player_choice = input("That's not a valid choice. Please try again: ")

      # check user's ans to the correct 
      player_ans_choice = question.choices[question_choices_keys.index(player_choice.upper())]
      correct_ans_choice = question_choices_keys[question.choices.index(question.correct_ans)]

      # if their's answer is correct, add money and move on to the next question
      if question.correct_ans == player_ans_choice:
        money_earned += prizes[i]
        if i == len(questions) - 1:
          print(f'You\'ve become a millionaire. Good luck in your next game :)')
          print(display_money_earned(money_earned))
          is_game_over = True
        else:
          print(f'\nYou are correct. Let\'s move on to the next question.')
          print(display_money_earned(money_earned))
      
      # if their's answer is incorrect, they only get $1000 and leave
      else:
        if money_earned > 1000:
          money_earned = 1000
        print(f'Oops, the correct answer is {correct_ans_choice}. {question.correct_ans}. Try again :(')
        print(display_money_earned(money_earned))
        is_game_over = True


def start():
  print('Welcome to Who Wants to be a Millionaire.')
  print('To win the game, you have to overcome 15 questions.')
  print('You will earn an amount of money as you answer a question correctly.')
  isConfirmed = input('If you answer all 15 questions correctly by typing your answer, you are a "millionaire". Are you ready to play? [Y/N]: ')
  if isConfirmed.lower() == 'y':
    display_questions()
  else: exit()

start()