import random
import sys

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'backside'

def main():
    print('''\n
    (H)it to take another card.
    (S)tand to stop taking cards.
    (D)ouble Down (on first play only) to double your bet.
        You can hit only one more time after doubling down.
    In the event of a tie, your bet is returned to you.
    The dealer stops hitting at 17.
    ''')

    money = 5000
    while True:
        if money <= 0:
            print("\nSorry, you're broke!")
            print("Good thing you weren't playing with real money!")
            print("Thanks for playing!")
            sys.exit()

        print("\nMoney: $", money)
        bet = get_bet(money)
        deck = get_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]
        print("\nBet: ", bet)
        
        while True:
            display_hands(player_hand, dealer_hand, False)
            print()
            if get_hand_value(player_hand) > 21:
                break
            
            move = get_move(player_hand, money - bet)
            if move == "D":
                add_bet = get_bet(min(bet, (money - bet)))
                bet += add_bet
                print("\nBet increased to {}.".format(bet))
                print("\nBet: $", bet)

            if move in ("H", "D"):
                new_card = deck.pop()
                rank, suit = new_card
                print("\nYou drew a {} of {}.".format(rank, suit))
                player_hand.append(new_card)

                if get_hand_value(player_hand) > 21:
                    continue

            if move in ("S", "D"):
                break

        if get_hand_value(player_hand) <= 21:
            while get_hand_value(dealer_hand) < 17:
                print("\nDealer hits...")
                dealer_hand.append(deck.pop())
                display_hands(player_hand, dealer_hand, False)
                
                if get_hand_value(dealer_hand) > 21:
                    break
                input("\nPress enter to continue...")
                print("\n\n")

        display_hands(player_hand, dealer_hand, True)
        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealer_hand)

        if dealer_value > 21:
            print("\nDealer busts! You win ${}!".format(bet))
            money += bet
        elif (player_value > 21) or (player_value < dealer_value):
            print("\nSorry, you lost this one!")
            money -= bet
        elif player_value > dealer_value:
            print("\nYou won ${}!".format(bet))
            money += bet
        elif player_value == dealer_value:
            print("\nIt's a push - your bet is returned to you!")

        input("\nPress Enter to continue...")
        print("\n\n")

def get_bet(max_bet):
    while True:
        print("\nHow much do you want to bet? ($1 - ${}, or QUIT)".format(max_bet))
        bet = input("> $").upper().strip()
        if bet == "QUIT":
            print("\nThanks for playing!")
            sys.exit
        if not bet.isdecimal():
            continue
        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet

def get_deck():
    deck =[]
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ("J", "Q", "K", "A"):
            deck.append((rank, suit))
    random.shuffle(deck) 
    return deck 

def display_hands(player_hand, dealer_hand, show_dealer_hand):
    print()
    if show_dealer_hand:
        print("\nDEALER:", get_hand_value(dealer_hand))
        display_cards(dealer_hand)
    else:
        print("DEALER: ???")
        display_cards([BACKSIDE] + dealer_hand[1:])

    print("PLAYER:", get_hand_value(player_hand))
    display_cards(player_hand)

def get_hand_value(cards):
    value = 0
    number_of_aces = 0
    for card in cards:
        rank = card[0]
        if rank == "A":
            number_of_aces += 1
        elif rank in ("K", "Q", "J"):
            value += 10
        else:
            value += int(rank)

    value += number_of_aces
    for i in range(number_of_aces):
        if value + 10 <= 21:
            value += 10
    return value

def display_cards(cards):
    rows = ["", "", "", "", ""]
    for i, card in enumerate(cards):
        rows[0] += " ___  "
        if card == BACKSIDE:
            rows[1] += "|## | "
            rows[2] += "|###| "
            rows[3] += "|_##| "
        else:
            rank, suit = card
            rows[1] += "|{} | ".format(rank.ljust(2))
            rows[2] += "| {} | ".format(suit)
            rows[3] += "|_{}| ".format(rank.rjust(2, "_"))

    for row in rows:
        print(row)

def get_move(player_hand, money):
    while True:
        moves = ["(H)it", "(S)tand"]
        if len(player_hand) == 2 and money > 0:
            moves.append("(D)ouble Down")
        move_prompt = ", ".join(moves) + "> "
        move = input(move_prompt).upper()
        if move in ("H", "S"):
            return move
        if move == "D" and "(D)ouble Down" in moves:
            return move

if __name__ == "__main__":
    main()
