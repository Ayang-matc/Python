## Gets new deck id

def newDeck(deckNumber):
    import requests

    myURL = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=' + deckNumber

    payload= {}
    headers= {}

    response = requests.request('GET', myURL, headers=headers, data=payload)

    deck= response.json()
    
    return deck['deck_id']
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

## Number of cards drawn

def numberOfCards():
    cards = input('How many cards would you like to draw from 0 to 5? ')
    isValidNumber = False
    while isValidNumber == False:
        if cards.isnumeric() == True:   
            if int(cards) >= 0 and int(cards) <= 5:
                isValidNumber = True
                return cards
            else:
                isValidNumber = False
                cards = input ('please enter valid number from 0 to 5. ')
            
        else:
            isValidNumber = False
            cards = input ('please enter valid number from 0 to 5. ')

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Number of decks shuffled

def getNumberofDecks():
    decks = input('How many decks would you like to draw from 1 to 3? ')
    isValidNumber = False
    while isValidNumber == False:
        if decks.isnumeric() == True:   
            if int(decks) >= 1 and int(decks) <= 3:
                isValidNumber = True
                return decks
            else:
                isValidNumber = False
                decks = input ('please enter valid number from 1 to 3. ')

        else:
            isValidNumber = False
            decks = input ('please enter valid number from 1 to 3. ')
           
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## prints rules

def printRules():
    print("The rules are to draw the highest score from the deck. GOOD LUCK!\n")

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## cards drawn

def cardsDrawn(dID, drawCount):
    import requests
    url = "https://deckofcardsapi.com/api/deck/" +dID+ "/draw/?count=" +drawCount

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    cardsDrawn = response.json()    
        
    return cardsDrawn['cards']

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## cards added up

def calculateScores(drawlist):
    score = 0
    for card in drawlist:
        value = card['value']
        if (value.isdigit()):
            score = score + int(value)
        else:
            score = score + 10
    return score
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## print cards 
    
def printCards(drawlist):
    for cards in drawlist:
        print (cards['value'] + ' of ' + cards['suit'].lower())

        
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def luckyCardGame():

    printRules()

    number_of_decks = getNumberofDecks()

    deck_id = newDeck(number_of_decks)

    num_of_cards_to_draw = numberOfCards()

    if int(num_of_cards_to_draw) == 0:
        print ("GAME OVER")

    else:
        
        cards_human_drawn = cardsDrawn(deck_id, num_of_cards_to_draw)
        cards_computer_drawn = cardsDrawn(deck_id, num_of_cards_to_draw)
        print ('\nYou have Drawn:')
        printCards(cards_human_drawn)
        print ('\nComputer has Drawn:')
        printCards(cards_computer_drawn)
        humanScore = str(calculateScores(cards_human_drawn))
        computerScore = str(calculateScores(cards_computer_drawn))
        print ('\nYour score is', humanScore, 'vs computer score is', computerScore)
        if (humanScore < computerScore):
            print ('Computer wins!')
        elif (humanScore == computerScore):
            print('It is a tie')
        else:
            print ('You Win!')



'Hello'    
    
    


    
