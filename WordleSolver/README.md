# NYT Wordle Solver

This program randomly selects a word from lessWords.txt, a file containing thousands of
valid words used by Wordle. The algorithm takes a specific starting word guess (the
default word is 'dealt', but this can be experimented with to see how it impacts
performance).

In order to maximize the likelihood of guessing the wordle within six guesses, this 
algorithm attempts to find the guess that is the best at reducing the pool of possible 
guesses for future attempts. To do this, the algorithm finds all possible responses to a 
guess, evaluates the new game state recursively, and sums the scores of all responses 
together, each weighted based on the likelihood of getting this response. This
algorithm’s running time is based on the number of possible guesses, and grows 
exponentially based on the number of guesses remaining in a game, so it is quite slow 
and can only be run in reasonable time with 4 or less guesses remaining.