import random
import time
import sys
import os

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
          p_type: The type of player, either 'Player' or 'Dealer'
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
            if self.type == 'DEALER' and self.dealer_show == False:
                ret_str += f'\nDEALER: ??, {attrs["hand"][1]}'
            else:
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
        for comparison against the dealer, in order to determine
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
        # suits = ['c', 'd', 'h', 's']
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
        print("Shuffling deck...")
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
      inital_deal -> Assign cards in proper order to player and dealer
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

    def initial_deal(self, player, dealer):
        '''
        initial_deal Method
        Parameters: player object, dealer object
        Description:
          Ensure that the initial deal is handled correctly.
          Deal order is player, dealer face down, player, dealer face up.
        '''
        self.shuffle()
        for _ in range(2):
            player.hand.append(self.get_card())
            dealer.hand.append(self.get_card())
        
        player.hand_value()
        dealer.hand_value()

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
      DEALER: 3♡, 4♢, 5♢, 9♢ (21)
    '''
    p_str = f"{player.type}: "
    p_str += f", ".join(item for item in player.hand)
    p_str += f" ({player.hand_strength})"
    print(p_str)


def show_table(player, dealer):
    '''
    show_table Method
    Parameters: player object, dealer object
    Description: Show the 'table' with the Dealer and Player hands
    '''
    clear()
    if dealer.dealer_show == False:
        print(dealer)
    else:
        show_hand(dealer)
    show_hand(player)


def main():
    '''
    Main function.
    Parameters: None
    Description: Play a game of Black Jack.
    Currently, no wagers are being made. 
    TODO:
    Add prompting/argparse for username
    add pickle for player.bank to track:
        wins, losses, pushes, and current bankroll.
    '''
    p1 = Player("player")
    d = Player("dealer")
    g = Game(**{"name": "Black Jack Game", 'num_decks': 3})
    g.initial_deal(p1, d)
    d.hand_value()
    has_player_acted = False    

    show_table(p1, d)

    if d.hand_strength == 21:
        if p1.hand_strength != 21:
            ''' Game is over, Dealer Wins. '''
            d.dealer_show = True
            show_table(p1, d)
            print("< Dealer dealt Black Jack >")
            sys.exit(1)
        else:
            d.dealer_show = True
            show_table(p1, d)
            print("== Even Money ==")
            sys.exit(2)

    while not p1.stand:
        '''
        Expectation is that the Player needs to finalize their
        action, before the Dealer takes any. In this case, we
        are going to follow that paradigm
        '''
        if not has_player_acted:
            if p1.hand_strength == 21:
                ''' Player has blackjack
                Check Dealer hand. If no face/ace card, player wins
                '''
                d.dealer_show = True
                d.stand = True
                p1.stand = True
                break

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
                break

            if p_input == 'f':
                p1.stand = True
                print("Player forfeits for half a bet")
                sys.exit()

            if p_input == 'h':
                card = g.get_card()
                p1.hand.append(card)
            
            p1.hand_value()
            if p1.hand_strength > 21:
                p1.busted = True
                show_table(p1, d)
                print("[ Player Busts ]")
                sys.exit()
            elif p1.hand_strength == 21:
                p1.stand = True

            has_player_acted = True
            
            show_table(p1, d)

    while p1.stand and not d.stand:
        ''' 
        Dealer now has to go through the process of drawing
        They can either tie, bust, or stand at 17+
        '''
        d.dealer_show = True
        show_table(p1, d)

        if d.hand_strength > 21:
            ''' Dealer Busts '''
            d.stand = True
            d.busted = True
            print("[ Dealer Busts! ]")
            break
        elif d.hand_strength >= 17:
            d.stand = True
            # show_hand(d)
            print("[ Dealer Stands ]")
            break
        else:
            ''' Dealer must have 16 or below '''
            d.hand.append(g.get_card())
            print("[ Dealer Hits ]")
            time.sleep(1)
            show_table(p1, d)
            d.hand_value()

    if p1.stand and d.stand:
        ''' Compare hands to determine winner'''
        d.dealer_show = True
        show_table(p1, d)

        if d.busted:
            print("++ Player Wins / Dealer busted ++")
            sys.exit()
        if p1.busted:
            print("-- Dealer Wins / Player busted --")
            sys.exit()
        if p1.hand_strength > d.hand_strength:
            print("++ Player Wins! ++")
        elif p1.hand_strength == d.hand_strength:
            print("> Push! <")
        else:
            print("< Dealer Wins! >")


if __name__ == "__main__":
    main()
