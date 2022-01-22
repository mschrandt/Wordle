import random

def loadWords():
    answerSpace = []
    allWords = []

    # Load all possible solution words
    with open("possiblewords.txt", "r", newline='') as wordFile:
        for word in wordFile:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                answerSpace.append(word)

    # Load all accepted words
    with open("acceptedwords.txt", "r", newline='') as wordFile:
        for word in wordFile:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                allWords.append(word)

    return answerSpace, allWords


def pickWord(allWords, answerSpace, ignoreChars):
    letterFrequency = {}

    if len(answerSpace) <= 2:
        return answerSpace[0]

    #Build letter frequency, ignoring characters that we already know
    for word in answerSpace:
        ignoreCharsCopy = ignoreChars
        for letter in word:
            if letter in ignoreCharsCopy:
                ignoreCharsCopy = ignoreCharsCopy.replace(letter,'',1)
            else:
                if letter not in letterFrequency:
                    letterFrequency[letter] = 0

                letterFrequency[letter] += 1

    bestWord = answerSpace[0]
    maxFrequency = 0

    # Score each word in full dictionary, ignoring letters we already know
    for word in allWords:
        currentFrequency = 0
        picked = set()
        ignoreCharsCopy = ignoreChars
        for letter in word:
            if letter in ignoreCharsCopy:
                ignoreCharsCopy = ignoreCharsCopy.replace(letter,'',1)
            else:
                if letter in picked:
                    continue
                picked.add(letter)
                if letter in letterFrequency:
                    currentFrequency += letterFrequency[letter]

        if currentFrequency > maxFrequency:
            maxFrequency = currentFrequency
            bestWord = word

    return bestWord

# Filter remaining answer space based on last guess & guess results
# Also update characters to ignore if any new letters were identified as part of the solution
def filterWords(words, guessWord, guessResult, ignoreChars):
    newIgnoreChars = ignoreChars
    for i in range(len(guessResult)):
        if guessResult[i] != 'x':
            if guessWord[i] in ignoreChars:
                ignoreChars = ignoreChars.replace(guessWord[i], '', 1)
            else:
                newIgnoreChars += guessWord[i]

    return [word for word in words if matchesGuessResult(word, guessWord, guessResult)], newIgnoreChars

# Return True if word fits the same pattern as the guess & guess results
# Example input:
# Word: ROBOT
# GuessWord: STARS
# GuessResult: xyxyx
# Returns True
def matchesGuessResult(word, guessWord, guessResult):

    for i in range(len(guessResult)):
        if guessResult[i] == 'g' and word[i] != guessWord[i]:
            return False
        elif guessResult[i] == 'y':
            if guessWord[i] == word[i]:
                return False
            elif guessWord[i] not in word:
                return False
        elif guessResult[i] == 'x':
            if word[i] == guessWord[i]:
                return False

            wrongLetterInstancesGuess = findLetterIndexesInWord(guessWord, guessWord[i])
            okCount = 0
            for j in wrongLetterInstancesGuess:
                if guessResult[j] != 'x':
                    okCount += 1
            wrongLetterInstancesWord = findLetterIndexesInWord(word, guessWord[i])
            if len(wrongLetterInstancesWord) > okCount:
                return False

    return True

def findLetterIndexesInWord(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]

# Return guess results to automate the game
def evaluateGuessResults(correctWord, guess):
    result = ""

    for i in range(len(correctWord)):
        if correctWord[i] == guess[i]:
            result += 'g'
        else:
            if guess[i] in correctWord:
                result += 'y'
            else:
                result += 'x'

    return result

def play(ai=False, verbose=False):
    guessResults = ''
    answerSpace, allWords = loadWords()
    numGuesses = 0
    correctWord = ''
    ignoreChars = ''

    if ai:
        correctWord = random.choice(answerSpace)
        print("Word is", correctWord)

    while len(answerSpace) > 0:
        if not ai or verbose:
            print(len(answerSpace), "words remaining in dict.")

        currentGuess = pickWord(allWords, answerSpace, ignoreChars)

        if not ai or verbose:
            print("Current guess:", currentGuess)

        if not ai:
            guessResults = input("Guess result: ")
        else:
            guessResults = evaluateGuessResults(correctWord, currentGuess)
            if verbose:
                print(guessResults)
        numGuesses += 1

        if guessResults == 'ggggg':
            break

        answerSpace, ignoreChars = filterWords(answerSpace, currentGuess, guessResults, ignoreChars)

    if guessResults == 'ggggg':
        print("Guessed in", numGuesses, "guesses.")
    else:
        print("Could not guess word:",correctWord)

    return numGuesses

totalGuesses = 0
maxGuessCount = 0
numGames = 1
random.seed(1)
for _ in range(numGames):
    currentGuessCount = play(False, False)
    totalGuesses += currentGuessCount
    if currentGuessCount > maxGuessCount:
        maxGuessCount = currentGuessCount

print("Avg guesses:",totalGuesses/numGames)
print("Worst case:",maxGuessCount,"guesses")
