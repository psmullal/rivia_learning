'''
Black Jack Simulator
--------------------
Rules:
- One player
    - Player may choose to hit, stay, double down, split
- Dealer
    - Dealer must hit <=16
    - Dealer must stay 17+
- Either Player or Dealer busts on 22+
- Aces are either 1 or 11
    - May change during the hand _EXCEPT_
        - if player chose to double down
- Double Down:
    - Only available as first choice
    - One more card is all the Player gets
- Dealing order: 
    - Player one card
    - Dealer one card
    - Player second card
    - Dealer second card
    
- Check for Black Jack
    - if Player has BJ, check Dealer
        - if Dealer showing an A, offer insurance/even money
            - if Dealer has black jack, push. 
        - else pay player 3:2
    - else prompt for hit/stay.
'''

import re
import random
import time

class Deck():
    '''
    Standard 52 card deck
    '''
    suits: list = ['c', 'd', 'h', 's']
    face_cards: list = ['J', 'Q', 'K', 'A', '2', '3',
                        '4', '5', '6', '7', '8', '9', '10']
    non_face_cards: list = list(range(2, 11))
    
    def __init__(self):
        self.shuffled = False
        self.single_deck: list = []
        cards  = [ f"{a}{b}" for a in self.face_cards for b in self.suits ]
        for c in cards:
            self.single_deck.append(c)

    def __repr__(self):
        if self.shuffled:
            return (f"Shuffled deck:\n{self.single_deck}")
        else:
            return("Standard 52 card deck.")

    def shuffle(self):
        print("Shuffling cards...")
        self.shuffled = True
        random.shuffle(self.single_deck)


class Game(Deck):
    def __init__(self):
        super().__init__()
        self.dealer_hand = []
        self.player_hand = []
        self.dealer_hand_value = 0
        self.player_hand_value = 0
        self.player_stands = False
        self.dealer_stands = False

    def __repr__(self):

        self.player_hand_value = self.hand_value(self.player_hand)
        self.dealer_hand_value = self.hand_value(self.dealer_hand)
        status_str = "----=[ Current Status ]=----"
        status_str += "\nDealer: "
        status_str += ", ".join(self.dealer_hand)
        status_str += f" ({self.dealer_hand_value})"
        status_str += "\nPlayer: "
        status_str += ", ".join(self.player_hand)
        status_str += f" ({self.player_hand_value})"
        status_str += "\n"

        return status_str

    def next_card(cards):
        while len(cards.single_deck) > 1:
            card = cards.single_deck.pop(1)
            # print(f"Cards remaining: {len(cards.single_deck)}")
            yield card

    def add_player_card(self, nc):
        self.player_hand.append(next(nc))
        self.player_hand_value = self.hand_value(self.player_hand)
        if self.player_hand_value > 21:
            self.show_winner()

    def add_dealer_card(self, nc):
        self.dealer_hand.append(next(nc))
        self.dealer_hand_value = self.hand_value(self.dealer_hand)
        if self.dealer_hand_value > 21:
            self.show_winner()


    def initial_deal(self, nc):
        for _ in range(2):
            self.add_player_card(nc)
            self.add_dealer_card(nc)
        
    def card_value(self, single_card):
        sc = single_card.strip('c').strip('d').strip('h').strip('s')
        # print(f"DEBUG: Single Card: {sc}")
        return sc

    def hand_value(self, cards: list):
        """ Process Hand """
        h_value = 0
        for dc in cards:
            v = self.card_value(dc)
            # print(f"DEBUG: Dealer Card: {v}")
            if v in 'KQJ':
                h_value += 10
            elif v == 'A':
                if h_value + 11 > 21:
                    h_value += 1
                else:
                    h_value += 11
            else:
                h_value += int(v)

        return h_value

    def show_winner(self):
        if self.player_hand_value > self.dealer_hand_value:
            return("Player Wins!")
        elif self.player_hand_value == self.dealer_hand_value:
            return("It's a push!")
        elif self.player_hand_value < self.dealer_hand_value:
            return("House wins =(")
        

    def dealer_action(self, nc):
        ''' 
        logic to determine if the dealer:
        - must hit
        - busts
        - beats player
        '''
        #### FIX THIS LOGIC
        if self.player_stands == True and self.dealer_stands == True:
            print(self.show_winner())
            return False

        if self.dealer_hand_value > 21:
            ''' Dealer loses '''
            self.dealer_stands = True
            print("Player Wins!!! Dealer busts")
            print(self.show_winner())
            return False

        elif self.dealer_hand_value >= 17 and self.dealer_hand_value <=21:
            ''' Dealer stands compare to player'''
            self.dealer_stands = True
            print(self.show_winner())
            return False
            
            
        if (self.dealer_hand_value < 17 and (
            self.dealer_hand_value < self.player_hand_value)):
            ''' Dealer is less than 17, must hit. '''
            self.add_dealer_card(nc)
            print("Dealer hits")
            time.sleep(2)
            print(self)
            self.dealer_action(nc)
        else:
            ''' Dealer wins?'''
            print(self.show_winner())
            return False


deck = Deck()
deck.shuffle()

game = Game()
nc = Game.next_card(deck)
game.initial_deal(nc)

print(game)

while True:
    command = input("Your action? ([S]tand, [H]it, [D]ouble Down: ").lower()
    if game.player_stands:
        if game.dealer_action(nc):
            pass
        break
    if command == 'h':
        game.add_player_card(nc)
        print(game)
    elif command == 'd':
        game.add_player_card(nc)
        game.player_stands = True
        print(game)
        # Can only take one card, so compare against dealer and exit
    elif command == 's':
        game.player_stands = True
        if game.dealer_action(nc):
            pass
        # Compare against Dealer/let Dealer draw.
    elif command == 'q':
        break
    else:
        print(f"{command} is not a valid command, please try again.")
    