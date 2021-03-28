#
# Hangman encapsulated into a class
#

import random
import webbrowser

hangman = ['---------- \n|\n|\n|\n|\n|\n|\n----------']
hangman += ['---------- \n|    | \n|\n|\n|\n|\n|\n----------']
hangman += ['---------- \n|    | \n|  (*-*) \n|\n|\n|\n|\n----------']
hangman += ['---------- \n|    | \n|  (*-*) \n|    | \n|    | \n|\n|\n----------']
hangman += ['---------- \n|    | \n|  (*-*) \n|   /| \n|    | \n|\n|\n----------']
hangman += ['---------- \n|    | \n|  (*-*) \n|   /|\ \n|    | \n|\n|\n----------']
hangman += ['---------- \n|    | \n|  (*-*) \n|   /|\ \n|    | \n|   / \n|\n----------']
hangman += ['---------- \n|    | \n|  (*-*) \n|   /|\ \n|    | \n|   / \ \n|\n----------']

class HangmanGame:
    """ an Hangman game that tracks, saves, and loads games
        If the hangman dies the game ends as a tie.
        Winning is when a person guesses the word 
    """

    def __init__(self):
        """ the constructor
              should include count of wins for each player
        """
        self.num_comp_wins = 0
        self.num_user_wins = 0
        self.num_ties = 0
  
    def __repr__(self):
        """ the representation function
              should return a string of some sort
        """
        s = ''
        s += "I have won" + str(self.num_comp_wins) + "games.\n"
        s += "You have won" + str(self.num_user_wins) + "games.\n"
        s += "We've tied" + str(self.num_ties) + "games.\n"
        return s

    def play_one_round(self):
        """ plays one game  of hangman"""
        
        wordBank = ["forty two", 'poptarts','three eyed alien','picobot','buzzwords','flopping','fluffiness','jotto','klutz'] # wordbank the game takes from
        # word bank AI uses to guess
        AIBank = ["forty two", 'thirty one', 'poptarts','three eyed alien','picobot', 'forty one', 'popsongs', 'hip hop','tacocat','buzzwords','flopping','fluffiness','jotto','klutz','lucky','mystify','onyx','nowadays']
        iGuess = 0                  # keeps count of the amount wrong guesses.
        guessed_let = ''
        # get the word for the game
        word = random.choice(wordBank)

        # keeps the guessing status of the word (starts blank)
        wordStatus = '-'*len(word)

        # print the initial round
        print()
        print(wordStatus)
        print()

        # run the game
        while True:
            #user's turn
            userg = input("Choose a letter: ")
            print()
            userg = userg.lower()                                   # change to lower case

            # do not allow repeat guesses
            while userg in guessed_let:                              # letter already guessed
                userg = input("Choose a letter: ")
                print()
                userg = userg.lower()
            guessed_let += userg

            if userg in word:
                wordStatus = self.updateWord(word, wordStatus, userg)   # update the word
            else:
                iGuess += 1

            print(hangman[iGuess])                                  # print hangman status 
            print()  

            if iGuess == 7:                                              #Hangman dies
                print("Hangman is dead, the game is tied.")
                print("The word was ", word)
                self.num_ties += 1
                self.play()

            print(wordStatus)                                       # show update
            print()

            guess = input("Do you want to guess the word? [y/n] ").lower()
            print()

            # sanity-check user's input
            while guess not in ['y','n']:
                print("    I didn't get what you meant by ", guess)
                guess = input("    Choose y or n: ").lower()
                print()

            # if they want to guess the word
            if guess == 'y':
                userWord = input("What is your guess? ")
                if userWord == word:                                # correct guess
                    print("You won!")
                    self.num_user_wins += 1
                    break
                else:
                    # print Game update
                    print("Oops,that's not the word.")
                    print(hangman[iGuess])                                  # print hangman status 
                    print()  
                    print(wordStatus)                                       # show update
                    print()                    

            # AI Turn

            aig = self.aiLet(wordStatus)

            print("AI's guess: ", aig)
            print()

            # do not allow repeat guesses
            while aig in guessed_let:                              # letter already guessed
                aig = self.aiLet(wordStatus)
                print("AI's guess: ", aig)
                print()

            guessed_let += aig

            if aig in word:
                wordStatus = self.updateWord(word, wordStatus, aig)   # update the word
            else:
                iGuess += 1

            print(hangman[iGuess])                                  # print hangman status 
            print()  

            if iGuess == 7:
                print("Hangman is dead, the game is tied.")
                print("The word was ", word)
                self.num_ties += 1
                self.play()

            print(wordStatus)                                       # show update
            print()

            aiWord = self.aiWor(wordStatus, AIBank)
            per_revealed = 0                                        # gauge for when AI starts guessing
            for c in wordStatus:
                if c != '-':
                    per_revealed += 1

            per_revealed = per_revealed/len(wordStatus)            


            if per_revealed >= 0.4:                             # start guessing when more than 40% of the word is revealled (confidence level > 40%)
                print("AI has a word guess: ", aiWord)
                print()
                if aiWord == word:                                # correct guess
                    print("Computer Won!")
                    self.num_comp_wins += 1
                    break
                else:
                    # print game update
                    print("AI was wrong,that's not the word.")
                    print(hangman[iGuess])                                  # print hangman status 
                    print()  
                    print(wordStatus)                                       # show update
                    print()                


    def aiLet(self, wordStatus):
        """ Uses rules of thumb to return ai's guess for the letter 
        """
        # Rule 1: guesses weighted based on how frequent a letter appears in english
        letters = list('eariotnslcudpmhgbfywkvxzjg') 
        freq = [11,9,8,8,7,7,7,6,5,4,4,3,3,3,3,2,2,2,2,1,1,1,0.3,0.3,0.2,0.2]

        return random.choices(letters, weights=freq)[0]

    def aiWor(self, wordStatus, AIBank):
        """ Uses rules of thumb to return ai's guess of the word
        """

        # Rule 2: Compare the length of the secret word with words in the AI's bank

        possibilties = []
        for w in AIBank:
            if len(w) == len(wordStatus):
                possibilties += [w]
            
        if len(possibilties) == 1:  #if there's only one match, choose that word
            return possibilties[0]  


        # if there's more than one match...
        # Rule 3: Check if the guessed letters align with each possible word, return the word that aligns

        for w in possibilties:
            pas = True
            for i in range(len(wordStatus)):
                if wordStatus[i] != '-':
                    if wordStatus[i] != w[i]:
                        pas = False
            if pas:
                return w



    def updateWord(self, word, wordStatus, letter):
        """ takes in word and if the guessed letter is in the word update the wordStatus"""
        wordList = list(wordStatus)         # split all the char (allows the changing of a single chars)
        if letter in word:                  # the letter is there
          for i in range(len(word)): 
            if word[i] == letter:
              wordList[i] = letter         # update the wordStatus
        newStatus = "".join(wordList)      # turn it back into a string
        return newStatus
            
    def pvp_game(self):
        """ Hosts a playver vs player 1 round game"""
        
        wordBank = ["forty two", 'poptarts','three eyed alien','picobot','buzzwords','flopping','fluffiness','jotto','klutz'] # wordbank the game takes from
        iGuess = 0                  # keeps count of the amount wrong guesses.
        guessed_let = ''
        # get the word for the game
        word = random.choice(wordBank)

        # keeps the guessing status of the word (starts blank)
        wordStatus = '-'*len(word)

        # print the initial round
        print()
        print(wordStatus)
        print()

        # run the game
        while True:
            #user's turn
            userg = input("Player 1 choose a letter: ")
            print()
            userg = userg.lower()                                   # change to lower case

            # do not allow repeat guesses
            while userg in guessed_let:                              # letter already guessed
                userg = input("Player 1 Choose a different letter: ")
                print()
                userg = userg.lower()
            guessed_let += userg

            if userg in word:
                wordStatus = self.updateWord(word, wordStatus, userg)   # update the word
            else:
                iGuess += 1

            print(hangman[iGuess])                                  # print hangman status 
            print()  

            if iGuess == 7:                                              #Hangman dies
                print("Hangman is dead, the game is tied.")
                print("The word was ", word)
                self.num_ties += 1
                self.play()

            print(wordStatus)                                       # show update
            print()

            guess = input("Do you want to guess the word? [y/n] ").lower()
            print()

            # sanity-check user's input
            while guess not in ['y','n']:
                print("    I didn't get what you meant by ", guess)
                guess = input("    Choose y or n: ").lower()
                print()

            # if they want to guess the word
            if guess == 'y':
                userWord = input("What is your guess? ")
                if userWord == word:                                # correct guess
                    print("You won!")
                    self.num_user_wins += 1
                    break
                else:
                    # print Game update
                    print("Oops,that's not the word.")
                    print(hangman[iGuess])                                  # print hangman status 
                    print()  
                    print(wordStatus)                                       # show update
                    print()                    


            #player's turn (player 2)
            playerg = input("Player 2 choose a letter: ")
            print()
            playerg = playerg.lower()                                   # change to lower case

            # do not allow repeat guesses
            while playerg in guessed_let:                              # letter already guessed
                playerg = input("Player 2 choose a different letter: ")
                print()
                playerg = playerg.lower()
            guessed_let += playerg

            if playerg in word:
                wordStatus = self.updateWord(word, wordStatus, playerg)   # update the word
            else:
                iGuess += 1

            print(hangman[iGuess])                                  # print hangman status 
            print()  

            if iGuess == 7:                                              #Hangman dies
                print("Hangman is dead, the game is tied.")
                print("The word was ", word)
                self.num_ties += 1
                self.play()

            print(wordStatus)                                       # show update
            print()

            pguess = input("Do you want to guess the word? [y/n] ").lower()
            print()

            # sanity-check user's input
            while pguess not in ['y','n']:
                print("    I didn't get what you meant by ", pguess)
                pguess = input("    Choose y or n: ").lower()
                print()

            # if they want to guess the word
            if pguess == 'y':
                playerWord = input("What is your guess? ")
                if playerWord == word:                                # correct guess
                    print("You won!")
                    self.num_comp_wins += 1
                    break
                else:
                    # print Game update
                    print("Oops,that's not the word.")
                    print(hangman[iGuess])                                  # print hangman status 
                    print()  
                    print(wordStatus)                                       # show update
                    print()

    def status(self):
        """ prints the current status """
        print("\n+ Current tally +")
        print("Comp/Player 2 wins:", self.num_comp_wins)
        print("  My/Player 1 wins:", self.num_user_wins)
        print("              Ties:", self.num_ties)
        print()

    def menu(self):
        """ prints the menu """
        print()
        self.status()
        print("Menu:")
        print("  (1) Continue our Hangman rivalry")
        print("  (2) Load our game")
        print("  (3) New game New Scores")
        print("  (4) Save our game")
        print("  (5) Player Vs. Player mode")
        print("  (8) Quit")
        print()
        uc = input("Your choice: ")
        try:
            uc = int(uc)  # try converting to an integer
            if uc not in [1,2,3,4,8,5]:  # Easter egs welcome!
                print("    Didn't recognize that input\n")
            else:
                return uc  # _must_ be a 1, 2, 4, 5,8

        except ValueError:  # it wasn't an integer...
            print("    Didn't understand that input\n")
            # print("The error was:", e)
        
        return self.menu()

    def play(self):
        """ hosts a series of games or turns """
        while True:
            userchoice = self.menu()  # prints the welcome and menu 

            if userchoice == 1:
                self.play_one_round()

            if userchoice == 8:
                print("Til next time!")
                break

            if userchoice == 4:
                self.save_game("gamefile.txt")

            if userchoice == 2:
                self.load_game("gamefile.txt")
                print("Welcome back!")

            if userchoice == 3:
                self.new_game()

            if userchoice == 5:
                self.pvp_game()

    def save_game(self, filename):
        """ save to a file """
        f = open(filename,"w")  # open file for writing
        data = [self.num_comp_wins, self.num_user_wins, self.num_ties]
        print(data,file=f)
        f.close()
        print(filename, " saved.")

    def load_game(self, filename):
        """ load from a file """
        f = open(filename,"r")  # open file for reading
        data = eval(f.read())   # evaluate the results as a Python object
        f.close()
        self.num_comp_wins = data[0]
        self.num_user_wins = data[1]
        self.num_ties = data[2]
        print(filename, " loaded.")
            
    def new_game(self):
        """ New game resets all tallies in the game to have a new fresh start"""
        self.num_comp_wins = 0
        self.num_user_wins = 0
        self.num_ties = 0


# create a game object, g
g = HangmanGame()
g.play()
