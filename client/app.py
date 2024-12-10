import time
import sys
from frontend import Frontend


class ChatApp:
    def __init__(self):
        self.frontend = Frontend()

    def handle_user_choice(self, choice):
        """Handles user input for menu choices."""
        if choice == "1":
            self.frontend.type_effect(self.frontend.print_colored("\nYou selected Log in.\n", 'yellow'))
            # Add login functionality here
        elif choice == "2":
            self.frontend.type_effect(self.frontend.print_colored("\nYou selected Sign in.\n", 'yellow'))
            # Add sign-in functionality here
        elif choice == "3":
            self.frontend.type_effect(self.frontend.print_colored("\nExiting... Goodbye!\n", 'red'))
            sys.exit(0)
        else:
            self.frontend.type_effect(self.frontend.print_colored("\nInvalid choice. Please choose again.\n", 'red'))

    def run(self):
        """Main loop of the application."""
        while True:
            self.frontend.display_banner()
            self.frontend.display_welcome_message()
            self.frontend.show_menu()
            choice = input("\nEnter your choice: ")
            self.handle_user_choice(choice)
            time.sleep(1)

# To run the app directly
if __name__ == "__main__":
    app = ChatApp()
    app.run()
