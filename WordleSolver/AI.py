#bot that will guess randomly from possible correct answers

import random
import game

class AIGuessing:
    def __init__(self):
        self.words = []


        with open("./wordleWords.txt","r") as fp:
            self.words = fp.readlines()
            for i in range(len(self.words)):
                self.words[i] = self.words[i][:5]
                
    
    def guessRandom(self, board):
        
        randomIndex = random.randrange(0,len(self.words))

        return self.words[randomIndex]

    def guessSmartRandom(self, board):
        
        possibleWords = []

        #find which letters we know are in the right position
        correctLetters = ['0', '0', '0', '0', '0']
        includedLetters = []
        unincludedLetters = []
        for guess in board:
            for x in range(5, 10):
                if (guess[x] == '2'):
                    #print('found ', guess[x-5], " at ", x-5)
                    correctLetters[x-5] = guess[x-5]
                if (guess[x] == '1'):
                    includedLetters.append(guess[x-5])
                if (guess[x] == '0'):
                    unincludedLetters.append(guess[x-5])

        #only add words that could be correct
        for word in self.words:
            add = True

            #use known letters in correct position
            for x in range (5):
                if (correctLetters[x] != '0' and word[x] != correctLetters[x]):
                    add = False

            #use known letters in incorrect position
            for letter in includedLetters:
                if (not word.__contains__(letter)):
                    add = False
            
            for letter in unincludedLetters:
                if (word.__contains__(letter)):
                    add = False
            
            if add:
                possibleWords.append(word)

        randomIndex = random.randrange(0,len(possibleWords))

        return possibleWords[randomIndex]

    def guessBasedOnLetterFrequency(self, board):
        
        possibleWords = self.PossibleWords(board, self.words)

        frequencies = {
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0,
    'e': 0,
    'f': 0,
    'g': 0,
    'h': 0,
    'i': 0,
    'j': 0,
    'k': 0,
    'l': 0,
    'm': 0,
    'n': 0,
    'o': 0,
    'p': 0,
    'q': 0,
    'r': 0,
    's': 0,
    't': 0,
    'u': 0,
    'v': 0,
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0}
        #count letters in all possible words
        for word in possibleWords:
            for x in range (5):
                frequencies[word[x]] += 1
        
        wordsScores = []

        correctLetters = ['0', '0', '0', '0', '0']
        includedLetters = []
        badLetters = []
        for guess in board:

            for x in range(5, 10):
                if (guess[x] == '2'):
                    #print('found ', guess[x-5], " at ", x-5)
                    correctLetters[x-5] = guess[x-5]
                if (guess[x] == '1'):
                    includedLetters.append(guess[x-5])
                if (guess[x] == '0'):
                    badLetters.append(guess[x-5])


        #score letters based on using more frequent letters. Ignores repeated letters to test for more
        #possible letters. low score = good choice
        for word in possibleWords:
            score = 0
            for x in range (5):
                score -= frequencies[word[x]]

                for y in range (x):
                    if (word[y] == word[x]):
                        score += frequencies[word[x]]
                        break
                
            wordsScores.append((score, word))
        word = min(wordsScores, key=lambda x: x[0])
        return word[1]

    def PossibleWords(self, board, currentOptions):

        possibleWords = []

        #find which letters we know are in the right position
        correctLetters = ['0', '0', '0', '0', '0']
        includedLetters = []
        badLetters = []
        for guess in board:

            for x in range(5, 10):
                if (guess[x] == '2'):
                    #print('found ', guess[x-5], " at ", x-5)
                    correctLetters[x-5] = guess[x-5]
                if (guess[x] == '1'):
                    includedLetters.append(guess[x-5])
                if (guess[x] == '0'):
                    badLetters.append(guess[x-5])

        #only add words that could be correct
        for word in currentOptions:
            add = True

            #use known letters in correct position
            for x in range (5):
                if (correctLetters[x] != '0' and word[x] != correctLetters[x]):
                    add = False
                    break

            #use known letters in incorrect position
            for letter in includedLetters:
                if (not word.__contains__(letter)):
                    add = False
                    break

            for guesses in board:
                if word == guesses[:5]:
                    add = False
                    break
                for x in range(5, 10):
                    if (guess[x] == '1' and word[x-5] == guess[x-5]):
                        add = False
                        break

            #discard words with bad letters
            for letter in badLetters:
                if (word.__contains__(letter) and not correctLetters.__contains__(letter) and not includedLetters.__contains__(letter)):
                    add = False
            
            

            if add:
                possibleWords.append(word)
        return possibleWords

    def GuessWithStarterWords(self, board, guessesRemaining):
        #guess coals, then niter, then use another algorithm for future guesses
        if (guessesRemaining == 6):
            return "dealt"
        elif (guessesRemaining == 5):
            return self.guessBasedOnLetterFrequency(board)
        else:
            possibleWords = self.PossibleWords(board, self.words)
            if (guessesRemaining == 4 and len(possibleWords) > 30):
                return self.guessBasedOnLetterFrequency(board)
            else:
                result, confidence = self.GuessHighestProbability(board, guessesRemaining, possibleWords)
                print("guess confidence: ", confidence)
                return result
        
    def GuessToMinimizePossibleWords(self, board, guessesRemaining):

        currentWords = self.PossibleWords(board, self.words)

    

        if (guessesRemaining == 6):
            return "dealt"
        elif (guessesRemaining == 5):
            return self.guessBasedOnLetterFrequency(board)
        elif (len(currentWords) == 1):
            return currentWords[0]
        else:
            #to check quality of a guess,
            #make that guess, and see how you many possible words are left if each word was the wordle
            #average those results
            bestScore = len(currentWords)
            word = 'splat'
            for guess in currentWords:
                score = 0
                for word in currentWords:
                    guessResult = self.checkGuess(word, guess)
                    board.append(guessResult)
                    score += len(self.PossibleWords(board, currentWords))
                    board.remove(guessResult)
                    if (score > bestScore * len(currentWords)):
                        break
                score = score / len(currentWords)
                if (score < bestScore):
                    word = guess
                    bestScore = score
                

            return word
        
    
    def GuessMinimizePossibleWords(self, board, guessesLeft):
        #final algorithm, 90% accuracy
        #first guess dealt, then 2 guesses based on letter frequency, then use a game tree for final guesses
        if (guessesLeft == 6):
            return "dealt"
        elif (guessesLeft > 3):
            return self.guessBasedOnLetterFrequency(board)
        else:
            possibleWords = self.PossibleWords(board, self.words)
            guess, confidence = self.GuessMinimizePossibleWordsHelper(board, guessesLeft, possibleWords)
            print("confidence of guess ", guess, ": ", confidence)
            return guess


    def GuessMinimizePossibleWordsHelper(self, board, guessesLeft, possibleWords):
        
        #finds average number of possible words after each guess, 
        #and returns the word that will minimize this.

        #can take ~30 seconds to find a guess with lots of possibleWords left, but hasn't taken
        #longer than this based on testing.

        #if no options, return last guess
        if (len(possibleWords) == 0):
            lastGuess = board[len(board)-1][:5]
            return (lastGuess, 1)

        #if one option, return it
        if (len(possibleWords) == 1):
            return (possibleWords[0], 1)
        
        #if last guess, guess randomly with low certainty
        if (guessesLeft == 1):
            randomIndex = random.randrange(len(possibleWords))
            return (possibleWords[randomIndex], len(possibleWords))
        

        bestScore = 9999999999999999
        bestGuess = "guess"

        #find guess with lowest average possible words left after guessing
        for guess in possibleWords:
            score = 0
            
            #find all possible colorKeys after this guess
            colorKeys = self.FindColorKeys(guess, board, possibleWords)

            for colorKey in colorKeys:
                #for each colorKey, find the average score after this response
                board.append(colorKey)
                newPossibleWords = self.PossibleWords(board, possibleWords)
                colorKeyScore = self.GuessMinimizePossibleWordsHelper(board, guessesLeft-1, newPossibleWords)
                board.remove(colorKey)

                #add to the score based on the frequency of this colorKey (given in self.FindColorKeys)
                score += colorKeyScore[1] * colorKeys[colorKey]
                
                #skip scoring if already a bad option
                if (score > bestScore):
                    break
            
            if (score < bestScore):
                bestScore = score
                bestGuess = guess

        return (bestGuess, bestScore) 
    
    def checkGuess(self, word, guess):

        #make a string to store the guess's accuracy
        colorKey = ""
        
        # finding the word's accuracy
        for x in range (5):
            if guess[x] == word[x]:
                colorKey += '2'
            elif guess[x] in word:
                #checking cases to display yellows correctly
                yellowNeeded = 0
                yellowCount = 0
                for i in range (x):
                    if (guess[x] == guess[i] and colorKey[i] == '1'):
                        yellowCount += 1
                for i in range (5):
                    if (guess[x] == word[i]):
                        yellowNeeded += 1
                        if (word[i] == guess[i]):
                            yellowNeeded -= 1
                    
                if (yellowNeeded > yellowCount):
                    colorKey += '1'
                else:
                    colorKey += '0'
            else:
                colorKey += '0'

        return guess + colorKey

    
    def FindColorKeys(self, guess, board, possibleWords):
        #finds all possible results after some guess, and likelihoods of each result

        colorKeys = {}
        for word in possibleWords:
            guessResult = self.checkGuess(word, guess)
            if (colorKeys.__contains__(guessResult)):
                colorKeys[guessResult] += 1
            else:
                colorKeys[guessResult] = 1
        #colorKeys = sorted(colorKeys, key=lambda x: colorKeys[x])


        return colorKeys
   
