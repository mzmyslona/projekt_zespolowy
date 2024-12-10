import sys
import time
import os
from termcolor import colored

# Function to clear the terminal (works for Unix-like systems, adjust for Windows)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to simulate typing effect
def type_effect(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Correct ASCII Art for the "Chat" banner
banner =r"""
   _____ _           _   
  / ____| |         | |  
 | |    | |_   _ ___| |_ 
 | |    | | | | / __| __|
 | |____| | |_| \__ \ |_ 
  \_____|_|\__,_|___/\__|
"""

def display_main_panel():
    clear()
    print(colored(banner, 'cyan'))
    type_effect(colored("Welcome to Chat!", 'yellow'), 0.05)
    type_effect(colored("Your communication starts here...\n", 'green'), 0.05)

def show_menu():
    type_effect(colored("\nPlease select an option:", 'magenta'))
    print("1) " + colored("Log in", 'blue'))
    print("2) " + colored("Sign in", 'blue'))
    print("3) " + colored("Exit", 'blue'))

def handle_user_choice(choice):
    if choice == "1":
        type_effect(colored("\nYou selected Log in.\n", 'yellow'))
        # Add login functionality here
    elif choice == "2":
        type_effect(colored("\nYou selected Sign in.\n", 'yellow'))
        # Add sign-in functionality here
    elif choice == "3":
        type_effect(colored("\nExiting... Goodbye!\n", 'red'))
        sys.exit(0)
    else:
        type_effect(colored("\nInvalid choice. Please choose again.\n", 'red'))

def main():
    while True:
        display_main_panel()
        show_menu()
        choice = input("\nEnter your choice: ")
        handle_user_choice(choice)
        time.sleep(1)

if __name__ == "__main__":
    main()
