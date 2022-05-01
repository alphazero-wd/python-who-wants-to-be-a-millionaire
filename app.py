# create questions using classes
# loop over the questions 
# if user answers correctly add bounties to them
# if they lost stop the game, and only receive a certain amount of bounty
# format the game
import random
from typing import List

class Question:
  def __init__(self, question, choices, correct_ans, difficulty):
    self.question: str = question
    self.choices: List[str] = choices
    self.correct_ans: str = correct_ans
    self.difficulty = difficulty
  
money_earned = 0
question_choices_keys = ['A', 'B', 'C', 'D']
valid_inputs = ['a', 'b', 'c', 'd', 'q', 'h']
fifty_fifty_left = 1
bounty = 100
questions: List[Question] = [
  Question(
    "Which of the following is the correct extension of the Javascript file?",
    ['.js', '.ts', '.🐍', '.bf'],
    '.js',
    'easy'
  ),
  Question(
    'Which line of JavaScript code includes the use of the ternary operator?',
    [
      'var answer = 100 φ 26;',
      'var answer = (age >= 16) ? "Drive" : "Walk";',
      'var answer = "Drive" || "Walk";',
      'var answer = (age >⎶ 16) ‽ "Drive" ܊ "Walk";'
    ],
    'var answer = (age >= 16) ? "Drive" : "Walk";',
    'easy'
  ),
  Question(
    'In HTML, how do you create an h2 element that says "CatPhotoApp"?',
    [
      '<header2>CatPhotoApp</header2>',
      '<h2>CatPhotoApp<h2>',
      'h2 = "CatPhotoApp"',
      '<h2>CatPhotoApp</h2>',
    ],
    '<h2>CatPhotoApp</h2>',
    'easy'
  ),
  Question(
    'What is the correct way to create a function in Javascript?',
    [
      'def myFunction():',
      'function myFunction():',
      'function myFunction() { }',
      'fn myFunction() end',
    ],
    'function myFunction() { }',
    'easy'
  ),
  Question(
    'Which symbols are used for a comment in JavaScript?',
    [
      '//',
      '\\\\',
      '\* *\ ',
      '¯\_(ツ)_/¯',
    ],
    '//',
    'easy'
  ),
  Question(
    'Of the following JavaScript if statements, which one correctly executes three instructions if the condition is true?',
    [
      'if (x < 0) a = b * 2; y = x; z = a – y;',
      'if{ (x < 0) a = b * 2; y = x; z = a – y ; }',
      'if (x < 0) { a = b * 2; y = x; z = a – y; }',
      'if (x < 0) { y = x; z = a – y * x + 1; }',
    ],
    'if (x < 0) { a = b * 2; y = x; z = a – y; }',
    'easy'
  ),
  Question(
    '''
    What is the output of the following Javascript code?
    console.log('3' + 4 + 5) 
    ''',
    ['345', 'TypeError: must be string, not number', '12', '39'],
    '345',
    'medium'
  ),
  Question(
    '''
    What is the output of the following Javascript code?
    var a = ['dog', 'cat', 'hen'];
    a[100] = 'fox';
    console.log(a.length); 
    ''',
    ['101', 'IndexError: list assignment index out of range', '4', 'undefined'],
    '101',
    'medium'
  ),
  Question(
    '''
    What is the output of the following Javascript code?
    var a = 10;
    console.log(a++)
    ''',
    ['10', 'NameError: name \'a\' is not defined', '11', 'undefined'],
    '10',
    'medium'
  ),
  Question(
    '''
    What is the output of the following Javascript code?
    function makePerson(first, last) {
      return {
        first: first,
        last: last,
        fullName: function() {
          return this.first + ' ' + this.last;
        }
      };
    }
    var s = makePerson('Simon', 'Willison');
    var fullName = s.fullName;
    console.log(fullName());
    ''',
    ['undefined undefined', 'Simon Willison', 'Willison Simon', 'null null'],
    'undefined undefined',
    'hard'
  ),
  Question(
    '''
    What is the output of the following Javascript code?
    function Person(name, age) {
      this.name = name
      this.age = age
    }
    var person1 = new Person('John', 30)
    var person2 = person1
    person2.age = 28
    console.log(person1.age)
    ''',
    ['28', '30', 'John', "undefined"],
    '28',
    'hard'
  ),
  Question(
  'Which of the following code returns the maximum number in an array in Javascript?',
  [
    'Math.max(array)',
    'Math.max(*array)',
    'Math.max.call(null, array)',
    'Math.max.apply(null, array)'
  ],
  'Math.max.apply(null, array)',
  'hard'
  ),
  Question(
    '''
    What is the output of the following Javascript code?
    function Person(name, age) {
      this.name = name
      this.age = age
    }
    var person1 = Person('John', 28)
    console.log(person1.name)
    ''',
    [
      'undefined', 
      'null', 
      'John', 
      'TypeError: can\'t access property \"name\" of \"person1\"'
    ],
    'undefined',
    'extreme'
  ),
  Question(
    '''
    What is the output of the following Javascript code?
    'use strict';
    function fun() { return this; }
    console.log(!fun() == 1); 
    ''',
    ['true', 'false', 'undefined', 'null'],
    'true',
    'extreme'
  ),
  Question(
    '''
    What is the output of the following Javascript code?
    var a = [-4, -7, 8, -9, 10, 20, -3, 2]
    a.map(function (num) {
      return -num
    })
    .sort(function(a, b) {
      return b - a
    })
    console.log(a)
    ''',
    [
      '[4, 7, -8, 9, -10, -20, 3, -2]',
      '[-4, -7, 8, -9, 10, 20, -3, 2]',
      '[20, 10, 8, 2, -3, -4, -7, -9]',
      '[9, 7, 4, 3, -2, -8, -10, -20]'
    ],
    '[-4, -7, 8, -9, 10, 20, -3, 2]',
    'extreme'
  )
]

# format the money earned
def display_money_earned():
  global money_earned
  def format_number():
    return "{:,}".format(money_earned)
  print(f'Money Earned: ${format_number()}\n')

def display_questions():
    global money_earned
    global is_game_over
    is_game_over = False
    for i, question in enumerate(questions):
      if is_game_over:
        break
      print(f'Question {i + 1} ({question.difficulty}): {question.question}')
      question.choices.sort(key=lambda _: 0.5 - random.random())

      # loop through the choices and shuffle them
      for index, choice in enumerate(question.choices):
        print(f'{question_choices_keys[index]}. {choice}')

      check_ans(i, question)

def check_ans(i, question: Question):
    global money_earned
    global is_game_over
    # check user's choice
    player_choice = input('Type in your choice [A/B/C/D], Q to leave the game or H to use 50/50 (case-insensitive): ')

    # if user enters invalid input
    while player_choice not in valid_inputs:
      player_choice = input("That's not a valid choice. Please try again: ")

    correct_ans_index = question.choices.index(question.correct_ans)

      # if user leaves, preserve their prize
    if player_choice.lower() == 'q':
      print('It\'s a safe choice to leave the game if you\'re uncertain of your answer. Good choice :)')
      display_money_earned()
      is_game_over = True
    
    # check user's ans to the correct 
    player_ans_index = question_choices_keys.index(player_choice.upper())
    player_ans = question.choices[player_ans_index]

    # if their's answer is correct, add money and move on to the next question
    if question.correct_ans == player_ans:
      global bounty
      money_earned += bounty
      bounty *= 2
      if i == len(questions) - 1:
        print(f'You\'ve become a millionaire. Good luck in your next game :)')
        display_money_earned()
        is_game_over = True
      else:
        print(f'\nYou are correct. Let\'s move on to the next question.')
        display_money_earned()
      
    # if their's answer is incorrect, they only get $1000 and leave
    else:
      if money_earned > 1000:
        money_earned = 1000
      print(f'Oops, the correct answer is {question_choices_keys[correct_ans_index]}. {question.correct_ans} :(')
      display_money_earned()
      is_game_over = True

def start():
  print('Welcome to Who Wants to be a Millionaire.')
  print('To win the game, you have to overcome 15 questions.')
  print('You will earn an amount of money as you answer a question correctly.')
  isConfirmed = input('If you answer all 15 questions correctly by typing your answer, you are a "millionaire". Are you ready to play? [y/n]: ')
  if isConfirmed.lower() == 'y':
    display_questions()
  else: exit()

start()