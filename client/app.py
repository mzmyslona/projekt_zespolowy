import sys
import time
import re  # Import regular expression library
from frontend import Frontend
from server_connection import ServerConnection
from user import User

class ChatApp:
    def __init__(self):
        self.frontend = Frontend()
        self.server_connection = ServerConnection()

    def login(self):
        """Handles user login."""
        self.frontend.type_effect(self.frontend.print_colored("\nLogin Panel\n", 'cyan'))
        username = input("Enter username: ")
        password = input("Enter password: ")

        user_to_auth = User(username, password)
        self.server_connection.log_in(user_to_auth)

        self.frontend.type_effect(self.frontend.print_colored("\nInvalid username or password.\n", 'red'))

    def is_valid_email(self, email):
        """Checks if the provided email is in a valid format."""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None

    def register(self):
        """Handles user registration and returns a User object."""
        self.frontend.type_effect(self.frontend.print_colored("\nRegistration Panel\n", 'cyan'))
        
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        email = input("Enter your email: ")

        # Validate if all fields are filled
        if not username or not password or not email:
            self.frontend.type_effect(self.frontend.print_colored("\nAll fields must be filled.\n", 'red'))
            return None

        # Validate email format
        if not self.is_valid_email(email):
            self.frontend.type_effect(self.frontend.print_colored("\nInvalid email format.\n", 'red'))
            return None

        # Create new User object
        new_user = User(username, password, email)
        self.users.append(new_user)
        self.frontend.type_effect(self.frontend.print_colored(f"\nRegistration successful! Welcome, {new_user.username}!\n", 'green'))
        return new_user

    def handle_user_choice(self, choice):
        """Handles user input for menu choices."""
        if choice == "1":
            self.login()
        elif choice == "2":
            new_user = self.register()  # Handle registration
            if new_user:
                self.logged_in_user = new_user
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
