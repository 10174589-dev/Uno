#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_1 = Motor(Ports.PORT1, False)
motor_5 = Motor(Ports.PORT5, True)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
   
# create events
FWD = Event()
RT = Event()
LT = Event ()

# Functions
def when_started():
    FWD.broadcast_and_wait()
    LT.broadcast_and_wait()
    FWD.broadcast_and_wait()
    RT.broadcast_and_wait()
    FWD.broadcast_and_wait()

def motor1_move_forward():
    # motor_1.spin_for(FORWARD, 425, DEGREES)   
     print('motor1 FWD 425')
def motor5_move_forward():
     #motor_1.spin_for(FORWARD, 220,DEGREES)
     print('motor5 FWD 425')
def motor1_turn_right():
    #motor_1.spin_for(FORWARD, 220, DEGREES)
    print('motor1 FWD 220')
def motor5_turn_right():
    #motor_5.spin_for(REVERSE, 220, DEGREES)
    print('motor5 REV 220')
def motor1_turn_left():
    #motor_1.spin_for(REVERSE, 220, DEGREES)
    print('motor1 REV 220')
def motor5_turn_left():
    #motor_5.spin_for(FORWARD< 220, DEGREES)
    print('motor5 FWD 220')

# Register allback functions to the events
FWD(motor1_move_forward)
FWD(motor5_move_forward) 
RT(motor1_turn_right)
RT(motor1_turn_right)
LT(motor5_turn_left)      
LT(motor5_turn_left)
wait(15, MSEC)

# Start the program!

# Brain Configuration
from vex import *
import random

# Initialize Brain
brain = Brain()

# --- UNO Game Logic & VEX Brain UI ---
COLORS = ["Red", "Yellow", "Green", "Blue"]
ACTION_CARDS = ["Skip", "Reverse", "Draw Two"]

def create_uno_deck():
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

def display_all_7_cards(hand):
    brain.screen.clear_screen()
    
    # Line 1: Title
    brain.screen.set_cursor(1, 1)
    brain.screen.print("START HAND (7)")
    
    # Lines 2-4: Pairs of cards
    for i in range(3):
        c1 = str(i * 2 + 1) + "." + format_short_card(hand[i * 2])
        c2 = str(i * 2 + 2) + "." + format_short_card(hand[i * 2 + 1])
        brain.screen.set_cursor(i + 2, 1)
        brain.screen.print(c1 + " " * (8 - len(c1)) + c2)
        
    # Line 5: Card 7
    c7 = "7." + format_short_card(hand[6])
    brain.screen.set_cursor(5, 1)
    brain.screen.print(c7)

def check_playable(card, top_card):
    if card['color'] is None:
        return True
    if top_card['color'] is not None and card['color'] == top_card['color']:
        return True
    if card['type'] == top_card['type']:
        return True
    return False

def select_top_card():
    # --- Display Color Selection Menu on Screen ---
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("SELECT COLOR:")
    brain.screen.set_cursor(2, 1)
    brain.screen.print("1.Red   2.Yel")
    brain.screen.set_cursor(3, 1)
    brain.screen.print("3.Grn   4.Blu")
    brain.screen.set_cursor(4, 1)
    brain.screen.print("5.Wild")
    
    selected_color = None
    while True:
        color_choice = input("Enter color (1-5): ")
        if color_choice == "1":
            selected_color = "Red"
            break
        elif color_choice == "2":
            selected_color = "Yellow"
            break
        elif color_choice == "3":
            selected_color = "Green"
            break
        elif color_choice == "4":
            selected_color = "Blue"
            break
        elif color_choice == "5":
            selected_color = None
            break
        else:
            brain.screen.set_cursor(5, 1)
            brain.screen.print("Err: Enter 1-5")

    selected_type = None
    if selected_color is None:
        # --- Display Wild Options on Screen ---
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("SELECT WILD:")
        brain.screen.set_cursor(2, 1)
        brain.screen.print("1. Wild")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("2. Wild Draw 4")
        
        while True:
            type_choice = input("Choice (1-2): ")
            if type_choice == "1":
                selected_type = "Wild"
                break
            elif type_choice == "2":
                selected_type = "Wild Draw Four"
                break
            else:
                brain.screen.set_cursor(5, 1)
                brain.screen.print("Err: Enter 1-2")
    else:
        # --- Display Card Type Options on Screen ---
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("CARD TYPE FOR " + selected_color.upper() + ":")
        brain.screen.set_cursor(2, 1)
        brain.screen.print("Types: 0-9")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Action: Skip,")
        brain.screen.set_cursor(4, 1)
        brain.screen.print("Reverse, Draw Two")
        
        while True:
            user_type = input("Card Type: ").strip().title()
            if user_type in ["0","1","2","3","4","5","6","7","8","9","Skip","Reverse"]:
                selected_type = user_type
                break
            elif user_type in ["Draw Two", "Draw 2", "D2"]:
                selected_type = "Draw Two"
                break
            else:
                brain.screen.set_cursor(5, 1)
                brain.screen.print("Invalid type!")

    top_card = {"color": selected_color, "type": selected_type}
    
    # --- Display Set Result on Screen ---
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("TOP CARD SET:")
    brain.screen.set_cursor(2, 1)
    brain.screen.print(format_full_name(top_card))
    
    return top_card

def player_turn_menu(player_hand, top_card):
    playable_indices = []
    for i in range(len(player_hand)):
        if check_playable(player_hand[i], top_card):
            playable_indices.append(i)

    # --- Display Turn Status on Screen ---
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("TOP: " + format_full_name(top_card))

    if len(playable_indices) == 0:
        brain.screen.set_cursor(2, 1)
        brain.screen.print("No playable card!")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Forced to DRAW.")
        return "DRAW"

    brain.screen.set_cursor(2, 1)
    brain.screen.print("Playable: " + str(len(playable_indices)) + " cards")
    brain.screen.set_cursor(3, 1)
    brain.screen.print("Check console/hand")
    brain.screen.set_cursor(4, 1)
    brain.screen.print("Enter choice (0-7)")
    
    while True:
        choice = input("Select card number (0 to draw): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if choice == "0":
                return "DRAW"
            elif 0 <= idx < len(player_hand):
                if idx in playable_indices:
                    return player_hand[idx]
                else:
                    brain.screen.set_cursor(5, 1)
                    brain.screen.print("Illegal card!")
            else:
                brain.screen.set_cursor(5, 1)
                brain.screen.print("Invalid choice!")
        else:
            brain.screen.set_cursor(5, 1)
            brain.screen.print("Enter a number!")

# --- Execution ---
def main():
    deck = create_uno_deck()
    custom_shuffle(deck)
    player_hand = deal_starting_hand(deck, 7)
    
    # Display Starting Hand on Brain Screen
    display_all_7_cards(player_hand)
    
    wait(3000, MSEC)  # 3 second pause to view initial hand layout
    
    top_card = select_top_card()
    
    wait(1500, MSEC)
    
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
        player_hand.remove(action)
        brain.screen.print("PLAYED CARD:")
        brain.screen.set_cursor(2, 1)
        brain.screen.print(format_full_name(action))

main()