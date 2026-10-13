
Volodymyr Balos
10:31 AM (7 minutes ago)
to me

# ==============================================================================
# VEX BRAIN SCREEN & BUTTON HARDWARE SPECIFICATIONS
# ==============================================================================
# Screen Text Dimensions (VEX EXP Brain):
#   - Text Lines: 5 Rows (Rows 1 to 5)
#   - Text Line Width: ~20 Characters (Cols 1 to 20)
#   - Screen Pixel Resolution: 160 x 128 pixels
#
# Available Hardware Input Buttons:
#   - brain.buttonLeft  : Cycles backward/left through menu options
#   - brain.buttonRight : Cycles forward/right through menu options
#   - brain.buttonCheck : Confirms selection
# ==============================================================================

#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

brain = Brain()

brain_inertial = Inertial()
motor_1 = Motor(Ports.PORT1, False)
motor_5 = Motor(Ports.PORT5, True)

wait(100, MSEC)

def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

initializeRandomSeed()
#endregion VEXcode Generated Robot Configuration

import random

# Hardware Button Handler
def wait_for_button_press():
    """Waits for a physical brain button press and returns 'LEFT', 'RIGHT', or 'CHECK'."""
    while brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing():
        wait(20, MSEC)
    
    while True:
        if brain.buttonLeft.pressing():
            while brain.buttonLeft.pressing(): wait(20, MSEC)
            return "LEFT"
        if brain.buttonRight.pressing():
            while brain.buttonRight.pressing(): wait(20, MSEC)
            return "RIGHT"
        if brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing(): wait(20, MSEC)
            return "CHECK"
        wait(20, MSEC)

# --- UNO Game Logic ---
COLORS = ["Red", "Yellow", "Green", "Blue"]
ACTION_CARDS = ["Skip", "Reverse", "Draw Two"]

def create_uno_deck():
    deck = []
    for color in COLORS:
        deck.append({"color": color, "type": "0"})
        for number in range(1, 10):
            deck.append({"color": color, "type": str(number)})
            deck.append({"color": color, "type": str(number)})
        for action in ACTION_CARDS:
            deck.append({"color": color, "type": action})
            deck.append({"color": color, "type": action})
            
    for _ in range(4):
        deck.append({"color": None, "type": "Wild"})
        deck.append({"color": None, "type": "Wild Draw Four"})
        
    return deck

def custom_shuffle(deck):
    deck_length = len(deck)
    for i in range(deck_length - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def deal_starting_hand(deck, num_cards=7):
    hand = []
    for _ in range(num_cards):
        if len(deck) > 0:
            hand.append(deck.pop(0))
    return hand

def format_full_name(card):
    if card['color'] is None:
        return card['type']
    return str(card['color']) + " " + str(card['type'])

def format_short_card(card):
    color_map = {"Red": "R", "Yellow": "Y", "Green": "G", "Blue": "B"}
    color_code = color_map.get(card['color'], "W")
    
    type_map = {
        "Skip": "Sk",
        "Reverse": "Rv",
        "Draw Two": "D2",
        "Wild Draw Four": "W4"
    }
    card_type = type_map.get(card['type'], card['type'])
    return str(color_code) + "-" + str(card_type)

def display_all_cards(hand):
    """Displays player's current hand across the 5-line screen."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("HAND (" + str(len(hand)) + " cards):")
    
    line = 2
    cards_str = ""
    for i, card in enumerate(hand):
        cards_str += str(i + 1) + "." + format_short_card(card) + " "
        if len(cards_str) >= 15 or i == len(hand) - 1:
            if line <= 5:
                brain.screen.set_cursor(line, 1)
                brain.screen.print(cards_str[:20])
                line += 1
                cards_str = ""

def check_playable(card, top_card):
    if card['color'] is None:
        return True
    if top_card['color'] is not None and card['color'] == top_card['color']:
        return True
    if card['type'] == top_card['type']:
        return True
    return False

# ==============================================================================
# NEW FUNCTIONS: LEGAL CARDS CHECK & MENU SELECTION
# ==============================================================================

def get_legal_cards(hand, top_card):
    """Returns a list of indices corresponding to legal cards in player_hand."""
    legal_indices = []
    for idx, card in enumerate(hand):
        if check_playable(card, top_card):
            legal_indices.append(idx)
    return legal_indices

def player_turn_menu(player_hand, top_card):
    """
    Displays a screen menu filtered to ONLY legal cards + DRAW option.
    Uses buttonLeft/buttonRight to navigate and buttonCheck to confirm.
    """
    legal_indices = get_legal_cards(player_hand, top_card)
    
    # Index 0 = "DRAW CARD", Index 1..N = Legal Card Options
    total_options = len(legal_indices) + 1
    selected_option = 0
    
    while True:
        brain.screen.clear_screen()
        
        # Row 1: Top Card Info (fitted for 20-char display width)
        brain.screen.set_cursor(1, 1)
        brain.screen.print("TOP: " + format_full_name(top_card)[:15])
        
        # Rows 2 & 3: Selection Details
        brain.screen.set_cursor(2, 1)
        if selected_option == 0:
            brain.screen.print("> [ DRAW CARD ]")
            brain.screen.set_cursor(3, 1)
            brain.screen.print("  Legal cards: " + str(len(legal_indices)))
        else:
            card_idx = legal_indices[selected_option - 1]
            card = player_hand[card_idx]
            brain.screen.print("> Play: " + format_short_card(card))
            brain.screen.set_cursor(3, 1)
            brain.screen.print("  Card #" + str(card_idx + 1) + " (" + str(selected_option) + "/" + str(len(legal_indices)) + ")")
        
        # Row 5: Hardware Controls Legend
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]:Nav  [Check]:OK")
        
        btn = wait_for_button_press()
        if btn == "LEFT":
            selected_option = (selected_option - 1) % total_options
        elif btn == "RIGHT":
            selected_option = (selected_option + 1) % total_options
        elif btn == "CHECK":
            if selected_option == 0:
                return "DRAW"
            else:
                chosen_card_idx = legal_indices[selected_option - 1]
                return player_hand[chosen_card_idx]

def select_top_card():
    color_options = ["Red", "Yellow", "Green", "Blue", "Wild"]
    color_idx = 0
    
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("SELECT START COLOR:")
        brain.screen.set_cursor(2, 1)
        brain.screen.print("< " + color_options[color_idx] + " >")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]:Nav  [Check]:OK")
        
        btn = wait_for_button_press()
        if btn == "LEFT":
            color_idx = (color_idx - 1) % len(color_options)
        elif btn == "RIGHT":
            color_idx = (color_idx + 1) % len(color_options)
        elif btn == "CHECK":
            selected_color = None if color_options[color_idx] == "Wild" else color_options[color_idx]
            break

    if selected_color is None:
        wild_options = ["Wild", "Wild Draw Four"]
        wild_idx = 0
        while True:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("SELECT WILD TYPE:")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("< " + wild_options[wild_idx] + " >")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("[L/R]:Nav  [Check]:OK")
            
            btn = wait_for_button_press()
            if btn == "LEFT":
                wild_idx = (wild_idx - 1) % len(wild_options)
            elif btn == "RIGHT":
                wild_idx = (wild_idx + 1) % len(wild_options)
            elif btn == "CHECK":
                selected_type = wild_options[wild_idx]
                break
    else:
        types_options = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]
        type_idx = 0
        while True:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("TYPE FOR " + selected_color.upper() + ":")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("< " + types_options[type_idx] + " >")
            brain.screen.set_cursor(5, 1)
            brain.screen.print("[L/R]:Nav  [Check]:OK")
            
            btn = wait_for_button_press()
            if btn == "LEFT":
                type_idx = (type_idx - 1) % len(types_options)
            elif btn == "RIGHT":
                type_idx = (type_idx + 1) % len(types_options)
            elif btn == "CHECK":
                selected_type = types_options[type_idx]
                break

    return {"color": selected_color, "type": selected_type}

# ==============================================================================
# MAIN GAME LOOP (TERMINATES WHEN HAND IS EMPTY)
# ==============================================================================

def main():
    deck = create_uno_deck()
    custom_shuffle(deck)
    player_hand = deal_starting_hand(deck, 7)
    
    display_all_cards(player_hand)
    wait(2500, MSEC)
    
    top_card = select_top_card()
    wait(1000, MSEC)
    
    # Game Loop repeats while player has remaining cards
    while len(player_hand) > 0:
        action = player_turn_menu(player_hand, top_card)
        
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        
        if action == "DRAW":
            if len(deck) > 0:
                drawn = deck.pop(0)
                player_hand.append(drawn)
                brain.screen.print("DREW CARD:")
                brain.screen.set_cursor(2, 1)
                brain.screen.print(format_full_name(drawn))
            else:
                brain.screen.print("DECK IS EMPTY!")
            wait(1500, MSEC)
        else:
            top_card = action  # Update top card to played card
            player_hand.remove(action)
            brain.screen.print("PLAYED CARD:")
            brain.screen.set_cursor(2, 1)
            brain.screen.print(format_full_name(top_card))
            brain.screen.set_cursor(3, 1)
            brain.screen.print("Cards Left: " + str(len(player_hand)))
            wait(1500, MSEC)

    # Game over win screen
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("*** YOU WIN! ***")
    brain.screen.set_cursor(3, 1)
    brain.screen.print("ALL CARDS PLAYED!")

main()