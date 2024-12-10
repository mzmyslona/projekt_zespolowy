import sys
import time
import os
from termcolor import colored

class Frontend:
    def __init__(self):
        self.banner = r"""
   ██████╗██╗  ██╗ █████╗ ████████╗
  ██╔════╝██║  ██║██╔══██╗╚══██╔══╝
  ██║     ███████║███████║   ██║   
  ██║     ██╔══██║██╔══██║   ██║   
  ╚██████╗██║  ██║██║  ██║   ██║   
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
"""

    def clear_screen(self):
        """Clears the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def type_effect(self, text, delay=0.04):
        """Simulates a typing effect for text."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def print_colored(self, text, color):
        """Returns colored text."""
        return colored(text, color)

    def display_banner(self):
        """Displays the main banner."""
        self.clear_screen()
        print(self.print_colored(self.banner, 'cyan'))

    def display_welcome_message(self):
        """Displays the welcome message."""
        self.type_effect(self.print_colored("Welcome to Chat!", 'yellow'), 0.05)
        self.type_effect(self.print_colored("Your communication starts here...\n", 'green'), 0.05)

    def show_menu(self):
        """Displays the menu options."""
        self.type_effect(self.print_colored("\nPlease select an option:", 'magenta'))
        print("1) " + self.print_colored("Log in", 'blue'))
        print("2) " + self.print_colored("Sign in", 'blue'))
        print("3) " + self.print_colored("Exit", 'blue'))
