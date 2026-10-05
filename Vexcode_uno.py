from vex import *
import random

# Initialize Brain
brain = Brain()

# --- Deck Configuration ---
COLORS = ["Red", "Yellow", "Green", "Blue"]
ACTION_CARDS = ["Skip", "Reverse", "Draw Two"]

def create_uno_deck():
    deck = []
    
    for color in COLORS:
        # One '0' card per color
        deck.append({"color": color, "type": "0"})
        
        # Two of each number '1' through '9'
        for number in range(1, 10):
            deck.append({"color": color, "type": str(number)})
            deck.append({"color": color, "type": str(number)})
            
        # Two of each action card per color
        for action in ACTION_CARDS:
            deck.append({"color": color, "type": action})
            deck.append({"color": color, "type": action})
            
    # Four Wild and Wild Draw Four cards
    for _ in range(4):
        deck.append({"color": None, "type": "Wild"})
        deck.append({"color": None, "type": "Wild Draw Four"})
        
    return deck

def custom_shuffle(deck):
    # MicroPython compatible Fisher-Yates shuffle
    deck_length = len(deck)
    for i in range(deck_length - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def create_shuffled_deck():
    deck = create_uno_deck()
    custom_shuffle(deck)
    return deck

# --- Main Program Execution ---
def main():
    shuffled_deck = create_shuffled_deck()
    
    print("=== UNO DECK (" + str(len(shuffled_deck)) + " cards) ===")
    
    for index in range(len(shuffled_deck)):
        card = shuffled_deck[index]
        color_name = card['color'] if card['color'] is not None else "Wild"
        card_str = color_name + " " + card['type']
        print("Card " + str(index + 1) + ": " + card_str)

    print("=============================")

# Run the program
main()
# Brain Configuration
from vex import *
import random

# Initialize Brain
brain = Brain()

# --- Deck Configuration ---
COLORS = ["Red", "Yellow", "Green", "Blue"]
ACTION_CARDS = ["Skip", "Reverse", "Draw Two"]

def create_uno_deck():
    deck = []
    
    for color in COLORS:
        # One '0' card per color
        deck.append({"color": color, "type": "0"})
        
        # Two of each number '1' through '9'
        for number in range(1, 10):
            deck.append({"color": color, "type": str(number)})
            deck.append({"color": color, "type": str(number)})
            
        # Two of each action card per color
        for action in ACTION_CARDS:
            deck.append({"color": color, "type": action})
            deck.append({"color": color, "type": action})
            
    # Four Wild and Wild Draw Four cards
    for _ in range(4):
        deck.append({"color": None, "type": "Wild"})
        deck.append({"color": None, "type": "Wild Draw Four"})
        
    return deck

def custom_shuffle(deck):
    deck_length = len(deck)
    for i in range(deck_length - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def create_shuffled_deck():
    deck = create_uno_deck()
    custom_shuffle(deck)
    return deck

def deal_starting_hand(deck, num_cards):
    hand = []
    for _ in range(num_cards):
        if len(deck) > 0:
            hand.append(deck.pop(0))
    return hand

def format_full_name(card):
    color_name = card['color'] if card['color'] is not None else "Wild"
    return color_name + " " + card['type']

def format_short_card(card):
    # Shorten color to 1 letter
    color_code = "W"
    if card['color'] == "Red":
        color_code = "R"
    elif card['color'] == "Yellow":
        color_code = "Y"
    elif card['color'] == "Green":
        color_code = "G"
    elif card['color'] == "Blue":
        color_code = "B"
        
    # Shorten action card type
    card_type = card['type']
    if card_type == "Skip":
        card_type = "Sk"
    elif card_type == "Reverse":
        card_type = "Rv"
    elif card_type == "Draw Two":
        card_type = "D2"
    elif card_type == "Wild Draw Four":
        card_type = "W4"
        
    return color_code + "-" + card_type

def display_all_7_cards(hand):
    brain.screen.clear_screen()
    
    # Row 1: Header (16 columns max)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("START HAND (7)")
    
    # Row 2: Cards 1 & 2
    c1 = "1." + format_short_card(hand[0])
    c2 = "2." + format_short_card(hand[1])
    brain.screen.set_cursor(2, 1)
    brain.screen.print(c1 + " " * (8 - len(c1)) + c2)
    
    # Row 3: Cards 3 & 4
    c3 = "3." + format_short_card(hand[2])
    c4 = "4." + format_short_card(hand[3])
    brain.screen.set_cursor(3, 1)
    brain.screen.print(c3 + " " * (8 - len(c3)) + c4)
    
    # Row 4: Cards 5 & 6
    c5 = "5." + format_short_card(hand[4])
    c6 = "6." + format_short_card(hand[5])
    brain.screen.set_cursor(4, 1)
    brain.screen.print(c5 + " " * (8 - len(c5)) + c6)
    
    # Row 5: Card 7
    c7 = "7." + format_short_card(hand[6])
    brain.screen.set_cursor(5, 1)
    brain.screen.print(c7)

# --- Main Program Execution ---
def main():
    deck = create_shuffled_deck()
    starting_hand = deal_starting_hand(deck, 7)
    
    # Print full names to the console
    print("=== STARTING HAND (7 Cards) ===")
    for index in range(len(starting_hand)):
        print("Card " + str(index + 1) + ": " + format_full_name(starting_hand[index]))
    print("===============================")
    
    # Render all 7 cards onto the single 5x16 screen layout
    display_all_7_cards(starting_hand)

# Run program
main()
