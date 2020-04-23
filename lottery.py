import random
import sys


class Lottery:
    """
    Create a Lottery class object
    Parameters: None
    Methods: none
    Attributes:
    winning_ticket: set containing 6 'random' integers
    powerball: int
    """
    def __init__(self: object):
        self.winning_ticket: set = generate_ticket()
        self.powerball: int = generate_powerball()


class Player:
    """
    Create a Player class object
    Parameters:
    name: string
    Methods: none
    Attributes:
    name: string
    player_ticket: list containing 6 'random' integers
    """
    def __init__(self: object, name: str):
        self.name = name
        self.player_ticket: set = generate_ticket()
        self.powerball: int = generate_powerball()


def generate_ticket() -> set:
    """
    Function that generates a list of random numbers
    Parameters: None
    Returns: List
    """
    ticket: set = []
    for _ in range(5):
        ticket.append(random.randrange(1, 71))
    return ticket


def generate_powerball() -> int:
    """ Function to generate a random number between 1 and 25 """
    return random.randrange(1, 26)


def did_i_win(state_ticket: list, my_ticket: list) -> int:
    '''
    Function to compare ticket values
    Parameters:
    state_ticket: list - 6 integers
    my_ticket: list - 6 integers
    Returns:
    retval: integer to determine success
      0: failure
      1: matched all 5
      99: matched all 5 and the powerball
    '''
    retval: int = 0  # default to non-winner
    if sorted(state_ticket.winning_ticket) == sorted(my_ticket.player_ticket):
        ''' I won something '''
        retval: int = 1
        if state_ticket.powerball == my_ticket.powerball:
            ''' I won it all!! '''
            retval = 99
    return retval


def print_stats(run_count: int, win_count: int, state_ticket: object,
                my_ticket: object):
    fmt = """\r---=[ Lottery Stats ]=---
    Total Number of runs: {}
    Total Number of wins: {}
    5 digit win percent:  {}
    -------------------------------
    """
    fivewins: float = (win_count/run_count)
    print(fmt.format(run_count, win_count, fivewins))


def main():
    '''
    Main Funtion
    Parameters: None
    Returns: int
    '''
    #  Run Once
    # state_ticket: object = Lottery()
    # my_ticket: object = Player('Patrick')
    # winner: int = did_i_win(state_ticket, my_ticket)

    #  Run repeatedly One State Lottery, multiple tickets
    state_ticket: object = Lottery()
    my_ticket: object = Player('Patrick')
    run_count: int = 0
    win_count: int = 0
    while True:
        run_count += 1
        winner: int = did_i_win(state_ticket, my_ticket)
        if winner == 1:
            win_count += 1
        elif winner == 99:
            print_stats(run_count, win_count, state_ticket, my_ticket)
            sys.exit(0)
        else:
            pass

        sys.stdout.write(f"\rRun: {run_count}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
