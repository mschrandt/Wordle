Development process documented here https://youtu.be/7Kfg5-JlA30

# Wordle
Run `python wordle.py` to play game

Input guess results in the form `xygxy`
- x represents a letter that is not in the answer word
- y represents a letter that is in the answer word but not in the correct position
- g represents a letter that is in the answer word and in the correct position

## Principles
- Top down approach
- Iterative approach

## Whiteboarding
Python

Code structure:
- Load in words
- Loop until we find the word:
  - Pick a word
  - Get results (as input)
  - Filter word list

## Recap
- Simple approach
- Automation                              Avg 6.07, Max 13
  - Improvement #1: Letter frequency        Avg 5.31, Max 13
  - Improvement #2: Don't filter pick list  Avg 5.12, Max 8
  - Improvement #3: Use game's dictionary   Avg 3.88, Max 6
  - Improvement #4: When down to 2, pick 1  Avg 3.74, Max 5
- Additional ideas?
  - Consider letter position
  - Pick most average letters
