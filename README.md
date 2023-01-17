# Who wants to be a Millionaire In Python

### Introduction

"Who wants to be a Millionaire" (WWTBAM) in Python is a terminal-based mini-app that simulates WWTBAM broadcasted on TV, but is written in Python and have some features omitted, such as no help.

### Rules (for people who don't know)

- A player starts the game with $0.
- The questions will about miscellaneous subjects, and will become increasingly difficult as the player progresses.
- If the player chooses the correct answer for a particular question, they will win an amount of money corresponding to that question.
- If the player gets one question incorrect, they will be forced to leave the game and lose a portion of their earned money.
- If the player gets stuck on a question, they can use 50:50 for that single question only to eliminate two wrong answers.
- If the player has used 50:50 and is still uncertain about the answer for a particular question, they can also choose to leave the game early to preserve their earned money.
- If the player successfully aces 15 questions, they will win $1,000,000 and be qualified as a "millionaire".

### How to play this game

- This WWTBAM game requires Internet connection as the questions will be fetched from an API.
- Ensure that you have Python (later than version 3.7) installed on your machine by typing the one of the commands below into the terminal, depending on your operating system

```bash
python --version # Windows
python3 --version # MacOS, Linux
```

- Clone the project by typing the command below into the terminal

```
git clone https://github.com/alphazero-wd/python-who-wants-to-be-a-millionaire.git
```

- Install the `requests` library using `pip`

```
pip install requests
```

- Execute the file `app.py` in the folder cloned from GitHub

```bash
python app.py # Windows
python3 app.py # MacOS, Linux
```

- Finally, follow what is instructed in the game and ENJOY :)
