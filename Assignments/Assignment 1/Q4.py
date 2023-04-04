import random

class TextGenerator:

    def __init__(self):
        # Save tuples, triplets and all words
        self.prefixDict = {}
        self.tupleDict = {}
        self.words = []

    def assimilateString(self, string):
        words = string.split()
        self.words = words
        # For each word
        for i, word in enumerate(words):
            # Out of words
            if i+2 >= len(words):
                break

            # Add triplet
            if (words[i], words[i+1]) in self.prefixDict.keys():
                self.prefixDict[(words[i], words[i+1])].append(words[i+2])
            else:
                self.prefixDict[(words[i], words[i+1])] = [words[i+2]]

            # Add tuple
            if words[i] in self.tupleDict.keys():
                self.tupleDict[words[i]].append(words[i+1])
            else:
                self.tupleDict[words[i]] = [words[i+1]]

    def assimilateText(self, filename):
        # Wrapper for assimilating full text file
        f = open(filename, 'r')
        fstring = f.read()

        self.assimilateString(fstring)
        f.close()

        return

    def generateText(self, length, startWord = None):
        if length <= 0:
            return ""

        if startWord == None:
            startWord = random.choice(self.words)
        elif startWord not in self.words:
            raise Exception("Unable to produce text with the specified start word.")

        if length == 1:
            return startWord

        sentance = [startWord]
        sentance.append(self.findNextWord(startWord))

        for i in range(length-2):
            sentance.append(self.findNextWord(sentance[-2], sentance[-1]))


        print (" ".join(sentance))

    def findNextWord(self, firstWord, secondWord = None):
        # Policy: Check for if triplet has been recognised, else check if tuple has been recognised, else generate random word from known list of words
        if secondWord == None:
            try:
                return random.choice(self.tupleDict[firstWord])
            except:
                return random.choice(self.words)

        try:
            return random.choice(self.prefixDict[(firstWord, secondWord)])
        except:
            try:
                return random.choice(self.tupleDict[firstWord])
            except:
                return random.choice(self.words)



## Test cases
# t = TextGenerator()
# t.assimilateText('Assignment 1/sherlock.txt')
# t.generateText(50, 'London')
