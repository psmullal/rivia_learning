import random
import time
import sys

class Player():
    '''Class Definition for Player'''
    
    def __init__(self, p_type='player', **kwargs):
        self.type = p_type.upper()
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.hand:list = []
        self.hand_strength: int = 0
        self.dealer_show = False
        self.stand = False

    def __repr__(self):
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

    def hand_value(self):
        """ Process Hand """
        h_value = 0
        for dc in self.hand:
            v = dc.strip('c').strip('d').strip('h').strip('s')
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

        self.hand_strength = h_value


class Deck():
    '''
    Standard 52 card deck
    Parameters: None
    '''
    suits: list = ['c', 'd', 'h', 's']
    face_cards: list = ['A', '2', '3', '4', '5', '6', '7',
                        '8', '9', 'T', 'J', 'Q', 'K']
    non_face_cards: list = list(range(2, 11))
 
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.shuffled = False
        self.single_deck: list = []
        cards  = [ f"{a}{b}" for a in self.face_cards for b in self.suits ]
        for c in cards:
            self.single_deck.append(c)

    def __repr__(self):
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
            print("Shuffling deck...")
            self.shuffled = True
            random.shuffle(self.single_deck)
    
    def next_card(self):
        while len(self.single_deck) > 1:
            card = self.single_deck.pop(1)
            # print((f"Drawing card: {card}"))
            # time.sleep(1)
            # print(f"-=[ {card} ]=-\nCards remaining: {len(self.single_deck)}")
            yield card


class Game(Deck):
    '''Class Definition for Game'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
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
        Deal order is player, dealer face down, player, dealer face up.
        '''
        self.shuffle()
        for _ in range(2):
            player.hand.append(self.get_card())
            dealer.hand.append(self.get_card())
        
        player.hand_value()
        dealer.hand_value()

    def get_card(self):
        deal_card = super().next_card()
        return next(deal_card)

    def compare_hands(self, h1, h2):
        pass

def show_hand(player):
    p_str = f"{player.type}: "
    p_str += f", ".join(item for item in player.hand)
    p_str += f" ({player.hand_strength})"
    print(p_str)

def main():
    ############ Tests and Status ############
    p1 = Player("player")
    d = Player("dealer")
    g = Game(**{"name": "Black Jack Game"})
    g.initial_deal(p1, d)
    d.hand_value()

    print(d)
    show_hand(p1)

    if d.hand_strength == 21:
        ''' Game is over, Dealer Wins. '''
        print("Dealer dealt Black Jack. Game over.")
        sys.exit(1)

    while not p1.stand:
        '''
        Expectation is that the Player needs to finalize their
        action, before the Dealer takes any. In this case, we
        are going to follow that paradigm
        '''

        prompt = "Option: [H]it, [S]tand, [D]ouble down, [Q]uit: "
        p_input = input(prompt).lower()
        if p_input in 'hsdq':
            if p_input == 'd':
                p1.stand = True
                p1.hand.append(g.get_card())
                show_hand(d)
            if p_input == 'h':
                p1.hand.append(g.get_card())
            if p_input == 's':
                p1.stand = True
                show_hand(d)
                break
            if p_input == 'q':
                break

            p1.hand_value()
            if p1.hand_strength > 21:
                print("** Player Busts!")
                break

            show_hand(d)
            show_hand(p1)

    while p1.stand and not d.stand:
        ''' 
        Dealer now has to go through the process of drawing
        They can either tie, bust, or stand at 17
        '''
        if d.hand_strength > 21:
            ''' Dealer Busts '''
            d.stand = True
            print("** Dealer Busts!")
            break
        elif d.hand_strength >= 17:
            d.stand = True
            print("** Dealer Stands.")
            break
        else:
            ''' Dealer must have 16 or below '''
            d.hand.append(g.get_card())
            print("** Dealer Hits")
            time.sleep(.5)
            d.hand_value()
        show_hand(d)
        show_hand(p1)

    if p1.stand and d.stand:
        ''' Compare hands to determine winner'''
        if p1.hand_strength > d.hand_strength:
            print("Player Wins!")
        elif p1.hand_strength == d.hand_strength:
            print("Push!")
        else:
            print("Dealer Wins!")

if __name__ == "__main__":
    main()
