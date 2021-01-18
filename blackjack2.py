'''
Blackjack simulator
take two
- player starts with 5k
- bet is asked at beginning of deal
- bet cannot exceed bank
- house bank is unlimited
- BJ pays 3:2 (or 1.5:1)
- player may double down, hit, stand, forfeit, insure against an Ace. splits are a future update
- house must hit 16 and less, stand on 17 and more.
- Per MGM rules, this is a 6 deck shoe.
- we have to re-shuffle the entire shoe when there are less than 20 cards left.
'''


import random
import time
import os
import pickle
import sys


class Player():
    '''
    Player Class
    Parameters: None
    Methods:
        __init__ -> Set up the base player
        __repr__ -> Display some debug info
        account_for_aces -> Process the hand value and evaluate Aces
        hand_value -> Determine 'value' of hand for comparison
    '''
    
    def __init__(self, p_type='player', **kwargs):
        '''
        Initialization Method
        Parameters:
            p_type: The type of player, either 'Player' or 'dlr'
          **kwargs: Any other info desired to pass in
            num_decks: The number of decks in this blackjack game.
        Description: Define instance of Player Class.
        '''
        self.type = p_type.upper()
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.hand:list = []
        self.hand_strength: int = 0
        self.dealer_show = False
        self.stand = False
        self.busted = False
        self.aces = 0
        self.bank = 5000 if p_type == 'player' else 1000000
        self.bet_amount = 20

    def __repr__(self):
        '''
        __repr__ method
        Parameters: self
        Description: returns string defining object
        '''
        ret_str = ''
        attrs = vars(self)
        
        for k, v in attrs.items():
            ret_str = ''
            if self.type == 'dlr' and self.dealer_show == False:
                ret_str += f'\nDEALER: ??, ' # {attrs["hand"][1]}'
            ret_str += '\n'.join('%-10s: %s' % item for item in attrs.items())            
            # ret_str += f'\n{border}\n'
        return ret_str

    def account_for_aces(self):
        '''
        account_for_aces Method
        Parameters: self
        Description: for 'fixing' Ace values, either 1 or 11 deterministic.
        If there are aces in the hand, but the value of 11 for the ace would
        cause the player to bust, reduce the value by 10 (resulting in a 
        value of 1), and reduce the number of aces calculated.
        '''

        while self.hand_strength > 21 and self.aces:
            self.hand_strength -= 10
            self.aces -= 1

    def hand_value(self):
        '''
        hand_value Method
        Paramters: self
        Description: Based on the 'cards' in the player's hand,
        assign the 'value' of that card to the total hand strength.
        This will calculate the total value of the hand and allow
        for comparison against the dlr, in order to determine
        the winner of the hand.
        '''
        h_value = 0
        self.aces = 0
        for dc in self.hand:
            v = dc[0]
            if v in 'KQJT':
                h_value += 10
            elif v == 'A':
                h_value += 11
                self.aces += 1
            else:
                h_value += int(v)

        self.hand_strength = h_value
        self.account_for_aces()


class Deck():
    '''
    Standard 52 card deck
    Parameters: None
    Optional: Pass 'num_decks' to create a multi-deck game.
    '''

    def __init__(self, **kwargs):
        '''
        Initialization Method
        Parameters:
          **kwargs: Any other info desired to pass in
        Description: Define instance of Deck Class.
        '''
        self.num_decks = 1
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.shuffled = False
        cards = ['A', 'K', 'Q', 'J', 'T', 9, 8, 7, 6, 5, 4, 3, 2]
        # suits = ['c', 'dlr', 'h', 's']
        # suits = ['\u2663', '\u2666', '\u2665', '\u2660'] # Black (solid) cards
        suits = ['\u2667', '\u2662', '\u2661', '\u2664'] # White cards
        '''        Clubs   Diamonds    Hearts   Spades '''
        self.single_deck = [ "{}{}".format(c, s) for c in cards for s in suits ]
        if self.num_decks:
            self.multi_deck = self.single_deck * self.num_decks
            print("There are {} decks for a total of {} cards.".format(
                self.num_decks, len(self.multi_deck)))

    def __repr__(self):
        '''
        __repr__ method
        Parameters: self
        Description: returns string defining object
        '''
        ret_str = ''
        attrs = vars(self)

        for k, v in attrs.items():
            ret_str = '==== Class "Deck" Dump ====\n'
            ret_len = len(ret_str)
            ret_str += '\n'.join('%-10s: %s' % item for item in attrs.items())
            border = '-' * ret_len
            ret_str += f'\n{border}\n'
        return ret_str

    def shuffle(self):
        '''
        shuffle Method
        Parameters: None
        Description: shuffles the deck and sets self.shuffle = True
        '''
        print(f"Shuffling deck... {len(self.multi_deck)}")
        self.shuffled = True
        random.shuffle(self.multi_deck)
            
    def next_card(self):
        '''
        next_card generator
        Parameters: None
        Description: Returns one card from the shuffled deck(s)
        '''
        while len(self.multi_deck) > 1:
            card = self.multi_deck.pop(1)
            yield card


class Game(Deck):
    '''
    Game Class Extends Deck Class
    Description: Defines the rules of the Game of Black Jack
    Methods:
        __init__ -> Create new instance
        __repr__ -> Return string of object definition
        inital_deal -> Assign cards in proper order to player and dlr
        get_card -> returns next card from next_card generator in parent
    '''
    def __init__(self, **kwargs):
        '''
        Initialization Method
        Parameters:
          **kwargs: Any other info desired to pass in
        Description: Define instance of Gane Class, extending the Deck Class.
        '''
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        '''
        __repr__ method
        Parameters: None
        Description: return string representation of the object
        '''
        ret_str = ''
        attrs = vars(self)
        for k, v in attrs.items():
            ret_str = '==== Class "Game" Dump ====\n'
            ret_len = len(ret_str)
            ret_str += '\n'.join('%-10s: %s' % item for item in attrs.items())
            border = '-' * ret_len
            ret_str += f'\n{border}\n'
        return ret_str

    def initial_deal(self, player, dlr):
        '''
        initial_deal Method
        Parameters: player object, dlr object
        Description:
            Ensure that the initial deal is handled correctly.
            Deal order is player, dlr face down, player, dlr face up.
        '''
        # self.shuffle()
        player.hand = []
        dlr.hand = []
        for _ in range(2):
            player.hand.append(self.get_card())
            dlr.hand.append(self.get_card())
        
        player.hand_value()
        dlr.hand_value()

    def get_card(self):
        '''
        get_card Method
        Parameters: None
        Description: return parent generator value
        '''
        deal_card = super().next_card()
        return next(deal_card)


def clear():
    '''
    clear Method
    Parameters: None
    Description: Clear the screen for output and draw heading
    Note: Works on Linux/Mac/Windows
    '''
    # check and make call for specific operating system 
    _ = os.system('clear' if os.name =='posix' else 'cls')
    print("---=[ Black Jack Game ]=---")


def show_hand(player):
    '''
    show_hand Method
    Parameters: player object
    Description: Display formatted string
    Example:
        dlr: 3♡, 4♢, 5♢, 9♢ (21)
    '''
    p_str = f"{player.type} ({player.bank}): "
    p_str += f", ".join(item for item in player.hand)
    p_str += f" ({player.hand_strength})"
    print(p_str)


def show_table(player, dlr):
    '''
    show_table Method
    Parameters: player object, dlr object
    Description: Show the 'table' with the dlr and Player hands
    '''
    clear()
    if dlr.dealer_show == False:
        show_hand(dlr)
    else:
        show_hand(dlr)
    show_hand(player)

def play_hand(p1, dlr):
    '''
    Set up new deal
    '''
    g.shuffle()
    g.initial_deal(p1, dlr)
    dlr.hand_value()
    has_player_acted = False
    dlr.dealer_show = False
    dlr.stand = False
    p1.stand = False
    show_table(p1, dlr)
    
    '''
    Let's go!
    '''
    if dlr.hand_strength == 21:
        if p1.hand_strength != 21:
            ''' Game is over, dlr Wins. '''
            dlr.dealer_show = True
            show_table(p1, dlr)
            print("< Dealer dealt Black Jack >")
            p1.bank -= p1.bet_amount
            return
        else:
            dlr.dealer_show = True
            show_table(p1, dlr)
            print("== Even Money ==")
            return

    while not p1.stand:
        '''
        Expectation is that the Player needs to finalize their
        action, before the dlr takes any. In this case, we
        are going to follow that paradigm
        '''
        if not has_player_acted:
            if p1.hand_strength == 21:
                ''' Player has blackjack
                Check dlr hand. If no face/ace card, player wins
                '''
                dlr.dealer_show = True
                dlr.stand = True
                p1.stand = True
                return

            prompt = "Option: [H]it, [S]tand, [D]ouble down, [F]orfeit: "
        else:
            prompt = "Option: [H]it, [S]tand: "

        p_input = input(prompt).lower()
        if p_input in 'hsdf':
            
            if p_input == 'd':
                p1.stand = True
                card = g.get_card()
                p1.hand.append(card)

            if p_input == 's':
                p1.stand = True
                

            if p_input == 'f':
                p1.stand = True
                print("Player forfeits for half a bet")
                p1.bank -= (p1.bet_amount/2)
                
            if p_input == 'h':
                card = g.get_card()
                p1.hand.append(card)
            
            p1.hand_value()

            if p1.hand_strength > 21:
                p1.busted = True
                show_table(p1, dlr)
                print("[ Player Busts ]")
                p1.bank -= p1.bet_amount
                return
            elif p1.hand_strength == 21:
                p1.stand = True

            has_player_acted = True
            
            show_table(p1, dlr)

    while p1.stand and not dlr.stand:
        ''' 
        dlr now has to go through the process of drawing
        They can either tie, bust, or stand at 17+
        '''
        dlr.dealer_show = True
        show_table(p1, dlr)

        if dlr.hand_strength > 21:
            ''' dlr Busts '''
            dlr.stand = True
            dlr.busted = True
            print("[ Dealer Busts! ]")
            p1.bank += p1.bet_amount
            # return
        elif dlr.hand_strength >= 17:
            dlr.stand = True
            # show_hand(dlr)
            print("[ Dealer Stands ]")
            # return
        else:
            ''' dlr must have 16 or below '''
            dlr.hand.append(g.get_card())
            print("[ Dealer Hits ]")
            time.sleep(1)
            show_table(p1, dlr)
            dlr.hand_value()

    if p1.stand and dlr.stand:
        ''' Compare hands to determine winner'''
        dlr.dealer_show = True
        show_table(p1, dlr)

        if dlr.busted:
            print("++ Player Wins / Dealer busted ++")
            p1.bank += p1.bet_amount
            return
        if p1.busted:
            print("-- Dealer Wins / Player busted --")
            p1.bank -= p1.bet_amount
            return
        if p1.hand_strength > dlr.hand_strength:
            print("++ Player Wins! ++")
            p1.bank += p1.bet_amount
        elif p1.hand_strength == dlr.hand_strength:
            print("> Push! <")
        else:
            p1.bank -= p1.bet_amount
            print("< Dealer Wins! >")

# player_name = input("Enter your name: ")
# kw_player = {'name': player_name,}
# p1 = Player('player', **kw_player)
p1 = Player('player')
dlr = Player('dealer')

# print(g)

'''
At this point, we have a player, a dlr, and a shoe with 6 randomized decks.
Time to have a single loop that continues until the player chooses to quit. 
We _should_ record their score, so we can pull it up later. This means we will
have to probably build in a reset_bank method.
Outer loop:
    - check number of cards left, > 20, continue
    - check player bank vs bet_amount. if bank > bet_amount, continue. 
        - else request reset.
    - reset players cards
    - reset dealers cards
    Inner Loop (dealing and player choices)
        - hand value (>21 is bust, lose bet and hand over, =21, auto-stand exit loop)
        - Hit - loop back to inner loop
        - Stand - Take no more cards, exit loop.
        - Double (2x bet, only one card) - deal one and loop back
        - Double for less ( 1.5 bet, only one card) - deal 1 and loop back
        - Forfeit (lose half bet and end hand)
        - (future) Split (only if a pair, unlimited splits, 
            - bet amount * number of splits)

    Second inner loop (dlr choices)
        - hand value
            - hand <=16, hit - loop back to second inner loop.
            - hand >=17, stand
            - hand = 21, win and player loses

    Compare Hands
        - player < dlr (dlr wins, lose money)
        - player > dlr (player wins, win money)
        - player == dlr (push, no money won)

    Return to Outer loop
'''
##  Outermost Loop
g = Game(**{"name": "Black Jack Game", 'num_decks': 6})
# print(f"There are {len(g.multi_deck)} cards in the shoe.")
while len(g.multi_deck) > 20:
    ''' 
    20 is an arbitrary number right now. Just something to trigger that
    we'dlr need to start a new shoe.`
    '''
    play_again = input("Deal? ")
    if play_again.upper() == 'Y':
        play_hand(p1, dlr)
    elif play_again.upper() == 'Q':
        sys.exit()
    