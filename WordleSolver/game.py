# WORDLE RULES
# 6 Guesses
# Yellow letter if in word
# Green if in correct postion

# in this implementation:
# lowercase letter if the letter is in the word
# uppercase letter if the letter is in the correct position

# Current Code State: Functional manually, no algorithms implemented yet

import random
import AI

class Wordle:
    def __init__(self):
        self.remainingGuesses = 6
        self.board = []
        self.word = ''
        self.words = []
        self.ai = AI.AIGuessing()
        

        print("Starting new game...")
        # Opens file with all 5 letter words
        with open("./wordleWords.txt","r") as fp:
            self.words = fp.readlines()
            for i in range(len(self.words)):
                self.words[i] = self.words[i][:5]
            
        # generates an integer to randomly choose a word
            randWord = random.randrange(0,len(self.words))
        # gathers line number and contents of line
            for lineNum, line in enumerate(self.words):
            # conditional sets word variable to contents of line
                if lineNum == randWord-1:
                    self.word = line
                    #self.word = "intro"
                    print("Today's random word is", self.word) #see the word at the start for debugging
                    break
        # now we have a randomly selected word as a string

    def makeGuess(self,guess):

        #make a string to store the guess's accuracy
        colorKey = ""
        
        # finding the word's accuracy
        for x in range (5):
            if guess[x] == self.word[x]:
                colorKey += '2'
            elif guess[x] in self.word:
                #checking cases to display yellows correctly
                yellowNeeded = 0
                yellowCount = 0
                for i in range (x):
                    if (guess[x] == guess[i] and colorKey[i] == '1'):
                        yellowCount += 1
                for i in range (5):
                    if (guess[x] == self.word[i]):
                        yellowNeeded += 1
                        if (self.word[i] == guess[i]):
                            yellowNeeded -= 1
                    
                if (yellowNeeded > yellowCount):
                    colorKey += '1'
                else:
                    colorKey += '0'
            else:
                colorKey += '0'

        if (colorKey == "22222"):
            return True

        #adding this guess to the Wordle's board
        #guesses are stored as strings with 5 characters as the guess and 5 characters as the accuracy (0 = gray, 1 = yellow, 2 = green)
        self.board.append(guess + colorKey)

        #removing one guess
        self.remainingGuesses -= 1

        #displaying the current state
        self.printBoard()

    def playManually(self):

        while(self.remainingGuesses > 0):
            
            #get player input
            validGuess = False
            while not validGuess:
                playerGuess = input("Please provide a 5 letter word: ")
                if self.words.__contains__(playerGuess):
                    validGuess = True

            #run the player's guess, record if they won or not
            win = self.makeGuess(playerGuess)
        

            #if they won, end the game
            if (win):
                print("you win! guesses used: ", 7 - self.remainingGuesses)
                break

        #if they use all guesses, you lose
        if (self.remainingGuesses == 0):
            print("you lose!")
            print("word was: ", self.word)
        print()

    def playUsingAI(self):

        while(self.remainingGuesses > 0):
            
            #get algorithm's play
            possibleWords = self.ai.PossibleWords(self.board, self.words)
            #print("possible words left before guess: ", len(possibleWords))

            AIguess = self.ai.GuessToMinimizePossibleWords(self.board, self.remainingGuesses) #only change this line to change which algorithm to use
            print("AI chooses:", AIguess)

            #run the AI's guess, record if they won or not
            win = self.makeGuess(AIguess)

            #if they won, end the game
            if (win):
                print("you win! guesses used: ", 7 - self.remainingGuesses, "\n")
                return True

        #if they use all guesses, they lose
        print("you lose!\n")
        return False
            


    def printBoard(self):
       for guess in self.board:
            for x in range (5):
                if (guess[x + 5] == '0'):
                    print("_", end=" ")
                elif (guess[x + 5] == '1'):
                    print(guess[x].lower(), end=" ")
                else:
                    print(guess[x].upper(), end=" ")
            print(" with guess:", end=" ")
            for x in range (5):
                print(guess[x], end="")
            print()
    
    


    
def main():


    #test the AI's win rate with 10 random words
    wins = 0
    games = 10

    for x in range (games):
        wordle = Wordle()
        success = wordle.playUsingAI()
        if (success):
            wins += 1
    print("current AI success rate: ", wins, "/", games)
    




if __name__ == "__main__":
    main()


