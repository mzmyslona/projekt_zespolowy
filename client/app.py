import sys
import time
from frontend import Frontend
from user import User

class ChatApp:
    def __init__(self):
        self.frontend = Frontend()
        # Predefined list of users for demonstration
        self.users = [
            User("john_doe", "password123", "john.doe@example.com"),
            User("jane_smith", "12345", "jane.smith@example.com")
        ]
        self.logged_in_user = None

    def login(self):
        """Handles user login."""
        self.frontend.type_effect(self.frontend.print_colored("\nLogin Panel\n", 'cyan'))
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Authenticate user
        for user in self.users:
            if user.username == username and user.password == password:
                self.logged_in_user = user
                self.frontend.type_effect(
                    self.frontend.print_colored(f"\nWelcome, {user.username}!\n", 'green')
                )
                return

        self.frontend.type_effect(self.frontend.print_colored("\nInvalid username or password.\n", 'red'))

    def handle_user_choice(self, choice):
        """Handles user input for menu choices."""
        if choice == "1":
            self.login()
        elif choice == "2":
            self.frontend.type_effect(self.frontend.print_colored("\nSign in functionality is under construction.\n", 'yellow'))
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

