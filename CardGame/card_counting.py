import csv
import random
import time
import sys

#creating a card
class card:
    def __init__(self, num, shape):
        self.num = num
        self.shape = shape
        self.color = self.cardColor()

    def cardColor(self):
        if self.shape == 'heart' or self.shape == 'diamond':
            return 'red'
        else:
            return 'black'

#creating a deck
class deck:
    def __init__(self):
        self.cards = []

    def count(self):
        return len(self.cards)
    
    def check(self):
        if len(self.cards) < 52:
            return (False, "You lost some cards somewhere.")
        
        hc, dc, sc, cc = 0,0,0,0
        
        for aCard in self.cards:
            if aCard.shape == 'heart':
                hc+=1
            elif aCard.shape == 'diamond':
                dc+=1
            elif aCard.shape == 'spade':
                sc+=1
            else:
                cc+=1
        if hc < 13:
            return(False, "Missing heart cards.")
        if dc < 13:
            return(False, "Missing diamond cards")
        if sc < 13:
            return(False, "Missing space cards.")
        if cc < 13:
            return(False, "Missing clover cards.")
        
        return(True, "Complete Deck!")

newDeck = deck()

print("Opening the deck of cards...\n")

#open the deck file and create deck of cards
with open('deck.csv') as cards:
    csv_reader = csv.reader(cards, delimiter=',')
    for row in csv_reader:
        newCard = card(row[0], row[1])
        newDeck.cards.append(newCard)
        print("|", end = ' ')
        sys.stdout.flush()
        time.sleep(0.01)


proceed, error = newDeck.check()

if proceed:
    #print the deck count to the screen
    print("\nYou've got a complete deck! There are", newDeck.count(), "cards.")

    print("\nShuffeling the deck!\n")
    #shuffle the deck!!!!
    random.shuffle(newDeck.cards)

    #show us all the cards
    #for theCard in newDeck.cards:
    #    print(theCard.num, theCard.shape, theCard.color)

    #count variables
    rc, bc, sc, cc, hc, dc = 0,0,0,0,0,0

    def IsItValid(GuessCard):
        cardFound = False
        for card in newDeck.cards:
            if card.color == GuessCard.color and card.shape == GuessCard.shape and card.num == GuessCard.num:
                cardFound = True
        
        if cardFound:
            return True
        else:
            print("\nThat's not a real card :( \n")
            return False
        

    randomCard = newDeck.cards[random.randint(0,51)]
    #print(randomCard.shape, randomCard.num, randomCard.color)

    guessedIt = False
    TryCount = 1

    while not guessedIt:

        guessNum = input("Guess the number? ")
        guessShape = input("Guess the shape? ")
        GuessCard = card(guessNum, guessShape)

        if IsItValid(GuessCard):
            if GuessCard.shape == randomCard.shape and GuessCard.num == randomCard.num:
                print("\n\nYou guessed it in", TryCount, "trys!")
                print("\nIt was the", randomCard.num, "of", randomCard.shape + "s\n\n")
                guessedIt = True
            else:
                print("\nTry again! #", TryCount)
                if TryCount <= 2:
                    print("\nHint: It's a", randomCard.shape)
                if TryCount <= 4 and TryCount >2:
                    print("\nHint: It's a", randomCard.num)
                guessedIt = False
                TryCount +=1
    
else:
    print(error)

