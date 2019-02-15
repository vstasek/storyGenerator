#----------------------------------------------------------------------
# StoryGenerator.py
# Victor Stasek
# 01/19/2013
#----------------------------------------------------------------------

'''StoryGenerator reads a training story from a file and then generates
a story based on it. For every pair of consecutive words in the file,
a list of the possible choice(s) of words that follows those two words
is kept as the story is read. To generate a story, the initial state is
(None, None) (so if you only train it with one story as the main function
does, the first two generated words, must be the first two words in the
sample story). After that, the story may vary.'''

import sys
import random

#----------------------------------------------------------------------

class StoryGenerator:

    '''Generates a random story based on training file(s)'''
    
    #------------------------------------------------------------------

    def __init__(self):

        '''
        pre: none
        
        post: empty StoryGenerator object initialized'''
        
        self.state = (None, None)
        self.model = {}
    
    #------------------------------------------------------------------

    def resetState(self):

        '''
        pre: none
        
        post: current state is set to (None, None) for adding a new
        story or generating a new story'''

        self.state = (None, None)
        
    #------------------------------------------------------------------

    def addWord(self, word):

        '''
        pre: none

        post: word is added to the model and the state is updated

        For example, if the state was ("the", "quick") and the word
        is "brown", then "brown" is added to the list of possible
        words that can follow ("the quick") and the state is now ("quick", "brown")'''

        # if current state is already in dictionary's keys
        if self.state in self.model:
            # adds word to list of possible proceeding words of current state
            self.model[self.state] += [word]
            
        # if current state is not in dictionary
        else:
            # adds a new key (current state) and maps it to word
            self.model[self.state] = [word]

        # updates self.state
        self.state = (self.state[1], word)

    #------------------------------------------------------------------

    def readFile(self, fname):

        '''
        pre: none

        post: each word in the file specified by fname is added to the
        model using the addWord method'''

        # opens a file and read its contents
        text = open(fname, 'r').read()
        # turns string into a list and iterates over it calling addWord
        # each time
        for word in text.split():
            self.addWord(word)
    
    #------------------------------------------------------------------

    def nextRandomWord(self):

        '''
        pre: readFile or addWord has been called to add data to the
        StoryGenerator object

        post: returns None if no next word for the current state
        otherwise returns a word (chosen at random from the possible
        words) and updates the state

        For example, if the state was ("the", "quick") and "brown" was
        the randomly chosen word, "brown" is returned and the state is
        now ("quick", "brown")'''

        # if current state is in dictionary's keys
        if self.state in self.model:
            # pick a word from list of values mapped to key
            word = random.choice(self.model[self.state])
            # update state
            self.state = (self.state[1], word)
            return word
        # if current state is not in dictinary's keys return None
        else:
            return None
    
    #------------------------------------------------------------------

    def generateStory(self, maxWords):

        '''pre: none

        post: based on the current state, a story of up to maxWords is
        generated and return as a string'''

        # establish accumulator - an empty string
        storyStr = ''

        for i in range(maxWords):
            # use nextRandomWord to generate a random word from list of
            # values mapped to current state
            word = self.nextRandomWord()
            # if word returned is not NoneType
            if word != None:
                # add word to accumulator with a space after to seperate words
                storyStr += word + ' '
            # if word returned is NoneType, quit loop
            else:
                break

        return storyStr
    
#----------------------------------------------------------------------

def main(argv):

    # if no command line argument with filename is provided,
    # ask user to enter one
    if len(argv) == 1:
        fname = input('enter training filename: ')
    else:
        fname = argv[1]

    # if no integer command line argument is provided,
    # ask user to enter one
    try:
        numWords = int(argv[2])
    except:
        numWords = int(input('enter maximum number of words: '))

    # generate story object and read file
    s = StoryGenerator()
    s.readFile(fname)

    # reset state and output generated story
    s.resetState()
    print(s.generateStory(numWords))                   

#----------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
