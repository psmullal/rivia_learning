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
import sys

class Player(object):
    hand:list  = []
    hand_value: int = 0

    def __init__(self, **kwargs):
        ''' Need to get two cards to start '''
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def add_card(self, nc):
        card = next(nc)
        self.hand.append(card)
        print(f'{self.name} ({self.type}) dealt: {card}')
        self.hand_value(self.hand)

    def hand_value(self, cards: list):
        """ Process Hand """
        h_value = 0
        for dc in cards:
            v = self.card_value(dc)
            # print(f"DEBUG: Card: {v} ({self.type}")
            if v in 'KQJT':
                h_value += 10
            elif v == 'A':
                if h_value + 11 > 21:
                    h_value += 1
                else:
                    h_value += 11
            else:
                h_value += int(v)

        self.hand_value = h_value
 
    def card_value(self, single_card):
        sc = single_card.strip('c').strip('d').strip('h').strip('s')
        # print(f"DEBUG: Single Card: {sc}")
        return sc


class Deck():
    '''
    Standard 52 card deck
    '''
    suits: list = ['c', 'd', 'h', 's']
    face_cards: list = ['J', 'Q', 'K', 'A', '2', '3',
                        '4', '5', '6', '7', '8', '9', 'T']
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
    players = []
    dealer = []

    def __init__(self):
        super().__init__()

    def __repr__(self):

        p.hand_value = p.hand_value(p.hand)
        d.hand_value = d.hand_value(d.hand)
        status_str = "----=[ Current Status ]=----"
        status_str += "\nDealer: "
        status_str += ", ".join(d.hand)
        status_str += f" ({d.hand_value})"
        status_str += "\nPlayer: "
        status_str += ", ".join(p.hand)
        status_str += f" ({p.hand_value})"
        status_str += "\n"

        return status_str

    # def hit(self, nc, p_or_d='player'):
    #     if p_or_d == 'player':
    #         self.player_hand_append(next(nc))
    #         self.player_hand_value = self.hand_value(self.player_hand)
    #     else:
    #         self.dealer_hand.append(next(nc))
    #         self.dealer_hand_value = self.hand_value(self.dealer_hand)

    # def stand(self, p_or_d='player'):
    #     if p_or_d == 'player':
    #         self.player_stands = True
    #     else:
    #         self.dealer_stands = True

    # def add_player_card(self, nc):
    #     self.player_hand.append(next(nc))
    #     self.player_hand_value = self.hand_value(self.player_hand)
    #     if self.player_hand_value > 21:
    #         ''' Player busted '''
    #         self.player_stands = True
    #         self.show_winner()

    # def add_dealer_card(self, nc):
    #     if self.dealer_hand_value > 21:
    #         ''' Dealer Busted '''
    #         self.dealer_stands = True
    #         self.show_winner()


    def initial_deal(self, nc, p: object, d: object):
        for _ in range(2):
            p.add_card(nc)
            d.add_card(nc)
        


    def show_winner(self, p:object, d: object):
        print(game)
        if self.player_hand_value > 21:
            ''' Player busts '''
            print('Player Busted, House Wins!')
            sys.exit(21)
        if self.dealer_hand_value > 21:
            ''' Dealer Busts '''
            print("Dealer Busted, Player Wins!")
            sys.exit(21)
        if self.dealer_hand_value == self.player_hand_value:
            ''' Push! '''
            print("PUSH!")
            sys.exit(1)
        if self.dealer_hand_value < self.player_hand_value:
            ''' Player wins '''
            print('Player Wins!')
            sys.exit(2)        
        if self.dealer_hand_value < self.player_hand_value:
            ''' House wins '''
            print('House Wins!')
            sys.exit(3)

    def dealer_action(self, nc):
        ''' 
        logic to determine if the dealer:
        - must hit
        - busts
        - beats player
        '''
        while True:
            if self.player_stands == True and self.dealer_stands == True:
                ''' compare and determine winnner'''
                self.show_winner()
            if self.player_stands == True:
                ''' Player has committed to their hand.'''
                # First check if dealer is less than 17. If so, we have to hit.
                if self.dealer_hand_value < 17:
                    self.add_dealer_card(nc)
                    print('Dealer Hits')
                    print(game)
                    time.sleep(.5)
                else:
                    if self.dealer_hand_value > self.player_hand_value:
                        ''' Dealer has beat Player '''
                        self.dealer_stands = True
                        self.show_winner()
                    elif self.dealer_hand_value == self.player_hand_value:
                        ''' Push '''
                        self.dealer_stands = True
                        self.show_winner()
                    else:
                        self.add_dealer_card(nc)
                        print(game)
                    return False
        game.show_winner()

def next_card(cards):
    while len(cards.single_deck) > 1:
        card = cards.single_deck.pop(1)
        # print(f"Cards remaining: {len(cards.single_deck)}")
        yield card



deck = Deck()
deck.shuffle()

game = Game()
p: object = Player(**{'name': "Player 1", 'type': 'player'})
d: object = Player(**{'name': "Dealer", 'type': 'dealer'})

nc = next_card(deck)
game.initial_deal(nc, p, d)

print(game)

sys.exit()
while game.dealer_stands == False and game.player_stands == False:
    if game.dealer_hand_value == 21 and len(game.dealer_hand) == 2:
        ''' Dealer has black jack. game over. player loses '''
        print(game)
        print(f'Dealer has Black Jack. Player loses.')
        break
    if game.player_hand_value == 21 and len(game.player_hand) == 2:
        ''' Player has won the game '''
        print(game)
        print('Player has won the game with a Black Jack.')
        break
    command = input("Your action? ([S]tand, [H]it, [Q]uit: ").lower()
    if game.player_stands and game.dealer_stands:
        break
    #     if game.dealer_action(nc):
    #         pass
    #     break
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
        print(game)
        if game.dealer_action(nc):
            pass
        # Compare against Dealer/let Dealer draw.
    elif command == 'q':
        break
    else:
        print(f"{command} is not a valid command, please try again.")
    