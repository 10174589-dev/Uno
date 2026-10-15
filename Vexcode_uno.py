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

# ==============================================================================
# ROBOT EVENT BROADCAST & MOTOR CONTROL
# ==============================================================================
FWD = Event()
RT = Event()
LT = Event()

def motor1_move_forward():
    motor_1.spin_for(FORWARD, 425, DEGREES, wait=False)

def motor5_move_forward():
    motor_5.spin_for(FORWARD, 425, DEGREES, wait=True)

def motor1_turn_right():
    motor_1.spin_for(FORWARD, 220, DEGREES, wait=False)

def motor5_turn_right():
    motor_5.spin_for(REVERSE, 220, DEGREES, wait=True)

def motor1_turn_left():
    motor_1.spin_for(REVERSE, 220, DEGREES, wait=False)

def motor5_turn_left():
    motor_5.spin_for(FORWARD, 220, DEGREES, wait=True)

FWD(motor1_move_forward)
FWD(motor5_move_forward)
RT(motor1_turn_right)
RT(motor5_turn_right)
LT(motor1_turn_left)      
LT(motor5_turn_left)
wait(15, MSEC)

# ==============================================================================
# PRIVACY & SCREEN DISPLAY FUNCTIONS
# ==============================================================================
def hide_hand_screen():
    """Hides the player's hand during transit to protect privacy."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("*** HAND HIDDEN ***")
    brain.screen.set_cursor(3, 1)
    brain.screen.print(" PRIVACY MODE ON ")

def display_uno_screen():
    """Displays layered UNO banner when player deposits 2nd-to-last card."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("====================")
    brain.screen.set_cursor(3, 1)
    brain.screen.print("    *** UNO! ***    ")
    brain.screen.set_cursor(5, 1)
    brain.screen.print("====================")

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

# ==============================================================================
# ROBOT NAVIGATION ROUTINES
# ==============================================================================
def drive_to_center(show_uno=False):
    """Drives to center table. Shows 'UNO!' overlay if triggered, else hides hand."""
    if show_uno:
        display_uno_screen()
    else:
        hide_hand_screen()
    wait(300, MSEC)
    FWD.broadcast_and_wait()
    FWD.broadcast_and_wait()

def drive_back_to_player():
    """Keeps hand hidden while returning to player."""
    hide_hand_screen()
    wait(300, MSEC)
   
    # 180 Degree Turn
    RT.broadcast_and_wait()
    RT.broadcast_and_wait()
   
    # Drive back
    FWD.broadcast_and_wait()
    FWD.broadcast_and_wait()
   
    # Turn back around to face starting position
    RT.broadcast_and_wait()
    RT.broadcast_and_wait()

# ==============================================================================
# HARDWARE BUTTON HANDLER
# ==============================================================================
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

# ==============================================================================
# UNO GAME LOGIC & DECK HELPERS
# ==============================================================================
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

def check_playable(card, top_card):
    if card['color'] is None:
        return True
    if top_card['color'] is not None and card['color'] == top_card['color']:
        return True
    if card['type'] == top_card['type']:
        return True
    return False

def get_legal_cards(hand, top_card):
    legal_indices = []
    for idx, card in enumerate(hand):
        if check_playable(card, top_card):
            legal_indices.append(idx)
    return legal_indices

def draw_multiple_cards(deck, player_hand, count=1):
    """Draws multiple cards one by one, displaying each drawn card step-by-step."""
    for i in range(count):
        if len(deck) > 0:
            drawn = deck.pop(0)
            player_hand.append(drawn)
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("DRAW CARD " + str(i + 1) + "/" + str(count) + ":")
            brain.screen.set_cursor(2, 1)
            brain.screen.print(format_full_name(drawn))
            brain.screen.set_cursor(4, 1)
            brain.screen.print("Hand size: " + str(len(player_hand)))
            wait(1500, MSEC)
        else:
            brain.screen.clear_screen()
            brain.screen.set_cursor(2, 1)
            brain.screen.print("DECK IS EMPTY!")
            wait(1500, MSEC)
            break

# ==============================================================================
# MENU SELECTION ROUTINES
# ==============================================================================
def choose_cards_to_draw():
    """Prompts player to select how many cards they want to draw (1 to 4)."""
    draw_options = ["1 Card", "2 Cards", "3 Cards", "4 Cards"]
    idx = 0
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("HOW MANY TO DRAW?")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("< " + draw_options[idx] + " >")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]:Nav  [Check]:OK")
       
        btn = wait_for_button_press()
        if btn == "LEFT":
            idx = (idx - 1) % len(draw_options)
        elif btn == "RIGHT":
            idx = (idx + 1) % len(draw_options)
        elif btn == "CHECK":
            return idx + 1  # Returns 1, 2, 3, or 4

def select_table_card():
    """Allows player to choose/set the card on the table."""
    color_options = ["Red", "Yellow", "Green", "Blue", "Wild"]
    color_idx = 0
   
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("CHOOSE TABLE COLOR:")
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

def player_turn_menu(player_hand, top_card):
    """
    First Screen: Prompts player to choose ATTACK or DRAW CARD.
    - If DRAW CARD: prompts for card count to draw.
    - If ATTACK: selects card from hand, then selects/sets card on table.
    """
    # --- Screen 1: First Choice (ATTACK vs DRAW CARD) ---
    turn_options = ["ATTACK", "DRAW CARD"]
    option_idx = 0
   
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("TOP: " + format_full_name(top_card)[:15])
        brain.screen.set_cursor(2, 1)
        brain.screen.print("CHOOSE ACTION:")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("< " + turn_options[option_idx] + " >")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]:Nav  [Check]:OK")
       
        btn = wait_for_button_press()
        if btn == "LEFT":
            option_idx = (option_idx - 1) % len(turn_options)
        elif btn == "RIGHT":
            option_idx = (option_idx + 1) % len(turn_options)
        elif btn == "CHECK":
            chosen_action = turn_options[option_idx]
            break

    # --- Choice A: DRAW CARD ---
    if chosen_action == "DRAW CARD":
        num_cards = choose_cards_to_draw()
        return ("DRAW", num_cards, None)

    # --- Choice B: ATTACK ---
    legal_indices = get_legal_cards(player_hand, top_card)
   
    if len(legal_indices) == 0:
        brain.screen.clear_screen()
        brain.screen.set_cursor(2, 1)
        brain.screen.print("NO LEGAL CARDS!")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Forced to DRAW.")
        wait(1500, MSEC)
        num_cards = choose_cards_to_draw()
        return ("DRAW", num_cards, None)

    # Step B1: Select card from player hand
    card_select_idx = 0
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("SELECT HAND CARD:")
       
        card_idx = legal_indices[card_select_idx]
        card = player_hand[card_idx]
       
        brain.screen.set_cursor(2, 1)
        brain.screen.print("> " + format_short_card(card))
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Card #" + str(card_idx + 1) + " (" + str(card_select_idx + 1) + "/" + str(len(legal_indices)) + ")")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]:Nav  [Check]:OK")
       
        btn = wait_for_button_press()
        if btn == "LEFT":
            card_select_idx = (card_select_idx - 1) % len(legal_indices)
        elif btn == "RIGHT":
            card_select_idx = (card_select_idx + 1) % len(legal_indices)
        elif btn == "CHECK":
            chosen_card_idx = legal_indices[card_select_idx]
            played_card = player_hand[chosen_card_idx]
            break

    # Step B2: Choose card on the table
    new_table_card = select_table_card()
   
    return ("ATTACK", played_card, new_table_card)

# ==============================================================================
# MAIN GAME LOOP
# ==============================================================================
def main():
    deck = create_uno_deck()
    custom_shuffle(deck)
    player_hand = deal_starting_hand(deck, 7)
   
    # Initial Hand Display at Start
    display_all_cards(player_hand)
    wait(2500, MSEC)
   
    top_card = select_table_card()
    wait(1000, MSEC)
   
    while len(player_hand) > 0:
        # 1. Display current hand before taking player turn
        display_all_cards(player_hand)
        wait(2000, MSEC)
       
        # 2. Get player action (ATTACK or DRAW)
        action_type, action_data, new_table_card = player_turn_menu(player_hand, top_card)
       
        # 3. Check for UNO (depositing 2nd-to-last card leaves 1 card)
        is_uno = (action_type == "ATTACK" and len(player_hand) == 2)
       
        if is_uno:
            brain.play_sound(SoundType.TADA)
       
        # 4. Drive to center table
        drive_to_center(show_uno=is_uno)
        wait(500, MSEC)
       
        brain.screen.clear_screen()
       
        # 5. Execute Action
        if action_type == "DRAW":
            draw_count = action_data
            draw_multiple_cards(deck, player_hand, count=draw_count)
        elif action_type == "ATTACK":
            played_card = action_data
            player_hand.remove(played_card)
            top_card = new_table_card  # Update top table card
           
            brain.screen.set_cursor(1, 1)
            brain.screen.print("ATTACKED WITH:")
            brain.screen.set_cursor(2, 1)
            brain.screen.print(format_full_name(played_card))
            brain.screen.set_cursor(3, 1)
            brain.screen.print("TABLE: " + format_full_name(top_card))
            brain.screen.set_cursor(4, 1)
            brain.screen.print("Cards Left: " + str(len(player_hand)))
            wait(1500, MSEC)
           
        # 6. Drive back to player (Keeps hand hidden during transit)
        drive_back_to_player()
       
        # 7. Show updated hand to player upon return
        display_all_cards(player_hand)
        wait(2000, MSEC)

    # Win Screen
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("*** YOU WIN! ***")
    brain.screen.set_cursor(3, 1)
    brain.screen.print("ALL CARDS PLAYED!")

main()



