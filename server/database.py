import sqlalchemy
from sqlalchemy.orm import sessionmaker
import models
import bcrypt
import datetime

class Database:
    def __init__(self):
        pass

    def db_connection(self):
        """Create and return a new database engine connection."""
        return sqlalchemy.create_engine(
            'postgresql+psycopg2://doadmin:AVNS_dHqY101i_n8FteRE3-j@messengerapp-db-do-user-18147258-0.j.db.ondigitalocean.com:25060/defaultdb'
        )

    def check_credentials(self, username_or_email, password):
        """Check if the provided username/email and password match an existing user."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        # Query the user by username or email
        user = session.query(models.Uzytkownicy).filter(
            (models.Uzytkownicy.nazwa_uzytkownika == username_or_email) |
            (models.Uzytkownicy.email == username_or_email)
        ).first()

        session.close()

        # If user exists, check the password
        if user and user.haslo:
            if bcrypt.checkpw(password.encode('utf-8'), user.haslo.encode('utf-8')):
                return True, "Credentials verified"
            else:
                return False, "Invalid password"
        elif user:
            return False, "User exists, but password is not set."
        else:
            return False, "User not found"

    def sign_up_user(self, username, email, password):
        """Register a new user with a username, email, and password."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        # Check for existing username or email
        existing_user = session.query(models.Uzytkownicy).filter(
            (models.Uzytkownicy.nazwa_uzytkownika == username) |
            (models.Uzytkownicy.email == email)
        ).first()

        if existing_user:
            session.close()  # Close the session
            return (False, "Username or email already exists.")

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = models.Uzytkownicy(
            nazwa_uzytkownika=username,
            email=email,
            haslo=hashed_password.decode('utf-8'),  # Store the hashed password
        )

        # Insert the new user into the database
        try:
            session.add(new_user)
            session.commit()
            return (True, "User added successfully!")
        except Exception as e:
            session.rollback()
            return (False, f"Error occurred during user creation: {str(e)}")
        finally:
            session.close()  # Ensure the session is closed

    def list_channels(self, username):
        """List all channels that the user belongs to."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        try:
            # Get the user based on username
            user = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == username).first()

            if not user:
                return False, "User not found."

            # Fetch all channels associated with the user
            channels = session.query(models.Kanaly).filter(models.Kanaly.uzytkownicy_kanalu.like(f'%{user.nazwa_uzytkownika}%')).all()

            if channels:
                # Return a list of channel names and owner IDs
                return True, [(channel.nazwa_kanalu, channel.id_wlasciciela) for channel in channels]  
            else:
                return False, "No channels found for this user."

        except Exception as e:
            # Log or handle the error as needed
            return False, f"Error occurred while listing channels: {str(e)}"
        
        finally:
            session.close()  # Always close the session
        
    def create_channel(self, channel_owner, channel_name, users):
        """Creates a new channel with the given owner and users."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        # Verify channel owner exists
        owner = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == channel_owner).first()
        if not owner:
            session.close()
            return False, "Channel owner not found."

        # Check if the channel name already exists
        existing_channel = session.query(models.Kanaly).filter(models.Kanaly.nazwa_kanalu == channel_name).first()
        if existing_channel:
            session.close()
            return False, "Channel name already exists."

        # Verify that all specified users exist
        for user in users:
            if not session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == user).first():
                session.close()
                return False, f"User '{user}' does not exist. Channel creation aborted."

        # Create the new channel
        new_channel = models.Kanaly(
            liczba_uzytkownikow=len(users),  # Set user count
            uzytkownicy_kanalu=', '.join(users),  # Store as a comma-separated list of usernames
            nazwa_kanalu=channel_name,
            id_wlasciciela=owner.id  # Foreign key link to owner
        )

        try:
            # Add the new channel to the session and commit
            session.add(new_channel)
            session.commit()
            return True, f"Channel '{channel_name}' created successfully!"
        except Exception as e:
            session.rollback()  # Roll back the session in case of error
            return False, f"Error occurred during channel creation: {str(e)}"
        finally:
            session.close()  # Always close the session

    # operacja autoryzowana - zawolac to moze tylko wlasciciel
    def remove_channel(self, channel_owner, channel_name):
        """Remove a channel only if the specified user is the owner."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        try:
            # Verify channel owner exists
            owner = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == channel_owner).first()
            if not owner:
                return False, "Channel owner not found."

            # Verify the channel exists and check if it belongs to the specified owner
            channel = session.query(models.Kanaly).filter(
                models.Kanaly.nazwa_kanalu == channel_name,
                models.Kanaly.id_wlasciciela == owner.id
            ).first()

            if not channel:
                return False, "Channel not found or you are not the owner."

            # Delete the channel from the database
            session.delete(channel)
            session.commit()

            return True, f"Channel '{channel_name}' removed successfully!"
        except Exception as e:
            session.rollback()  # Roll back in case of error
            return False, f"Error occurred during channel removal: {str(e)}"
        finally:
            session.close()  # Always close the session

    # operacja autoryzowana - tylko wlasciciel kanalu bedzie mogl dodac uzytkownikow
    def add_channel_member(self, channel_owner, channel_name, username):
        """Add a member to the specified channel if the channel owner is valid."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        # Verify the channel owner exists
        owner = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == channel_owner).first()
        if not owner:
            session.close()
            return False, "Channel owner not found."

        # Verify the channel exists
        channel = session.query(models.Kanaly).filter(
            models.Kanaly.nazwa_kanalu == channel_name,
            models.Kanaly.id_wlasciciela == owner.id
        ).first()
        
        if not channel:
            session.close()
            return False, "Channel not found or you are not the owner."

        # Verify the user to be added exists
        new_member = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == username).first()
        if not new_member:
            session.close()
            return False, f"User '{username}' does not exist."

        # Check if the specified user already exists in the channel's user list
        current_users = channel.uzytkownicy_kanalu.split(', ') if channel.uzytkownicy_kanalu else []
        
        if username in current_users:
            session.close()
            return False, f"User '{username}' is already a member of the channel."

        # Update the channel_users field
        current_users.append(username)  # Add the new user to the list
        channel.uzytkownicy_kanalu = ', '.join(current_users)  # Update the channel_users representation
        
        try:
            # Commit the changes to the session
            session.commit()
            return True, f"User '{username}' added to channel '{channel_name}' successfully!"
        except Exception as e:
            session.rollback()
            return False, f"Error occurred during adding user to channel: {str(e)}"
        finally:
            session.close()  # Always close the session

    def remove_channel_member(self, channel_owner, channel_name, username):
        """Remove a member from the specified channel if the channel owner is valid."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        # Verify the channel owner exists
        owner = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == channel_owner).first()
        if not owner:
            session.close()
            return False, "Channel owner not found."

        # Verify the channel exists and check if it belongs to the specified owner
        channel = session.query(models.Kanaly).filter(
            models.Kanaly.nazwa_kanalu == channel_name,
            models.Kanaly.id_wlasciciela == owner.id
        ).first()

        if not channel:
            session.close()
            return False, "Channel not found or you are not the owner."

        # Check if the user to be removed is the owner - prevent owner removal
        if username == channel_owner:
            session.close()
            return False, "The channel owner cannot be removed from the channel."

        # Verify that the specified user exists in the channel's user list
        current_users = channel.uzytkownicy_kanalu.split(', ') if channel.uzytkownicy_kanalu else []
        
        if username not in current_users:
            session.close()
            return False, f"User '{username}' is not a member of channel '{channel_name}'."

        # Remove the user from the channel's user list
        current_users.remove(username)  # Remove the user from the list
        channel.uzytkownicy_kanalu = ', '.join(current_users)  # Update the channel_users representation

        try:
            # Commit the changes to the session
            session.commit()
            return True, f"User '{username}' removed from channel '{channel_name}' successfully!"
        except Exception as e:
            session.rollback()  # Roll back in case of error
            return False, f"Error occurred during removing user from channel: {str(e)}"
        finally:
            session.close()  # Always close the session

    def send_message(self, sender_username, channel_name, message_content):
        """Send a message to a specified channel from the given user only if the user is a member of the channel."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        # Verify sender exists
        sender = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == sender_username).first()
        if not sender:
            session.close()
            return False, "Sender not found."

        # Verify the channel exists
        channel = session.query(models.Kanaly).filter(models.Kanaly.nazwa_kanalu == channel_name).first()
        if not channel:
            session.close()
            return False, "Channel not found."

        # Check if sender is a member of the channel
        current_users = channel.uzytkownicy_kanalu.split(', ') if channel.uzytkownicy_kanalu else []
        if sender.nazwa_uzytkownika not in current_users:
            session.close()
            return False, f"User '{sender.nazwa_uzytkownika}' is not a member of channel '{channel_name}'. Cannot send message."
        
        # Create a new message record
        new_message = models.Wiadomosci(
            nadawca_wiadomosci=sender.id,  # Set the sender ID
            kanal_odbiorcy=channel.id,  # Set the recipient to the channel ID
            data_wyslania=datetime.datetime.utcnow(),  # Current timestamp
            zawartosc=message_content.encode('utf-8')  # Store message content as binary data
        )

        try:
            # Add the new message to the session and commit
            session.add(new_message)
            session.commit()
            return True, f"Message sent to channel '{channel_name}' successfully!"
        except Exception as e:
            session.rollback()  # Roll back in case of error
            return False, f"Error occurred while sending the message: {str(e)}"
        finally:
            session.close()  # Always close the session


    # operacja autoryzowana - tylko wlasciciel kanalu bedzie mogl usunac uzytkownikow

    def channel_length(self, channel_owner, channel_name):
        """Return the number of messages in the specified channel."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        # Verify channel owner exists
        owner = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == channel_owner).first()
        if not owner:
            session.close()
            return False, "Channel owner not found."

        # Verify the channel exists and check if it belongs to the specified owner
        channel = session.query(models.Kanaly).filter(
            models.Kanaly.nazwa_kanalu == channel_name,
            models.Kanaly.id_wlasciciela == owner.id
        ).first()

        if not channel:
            session.close()
            return False, "Channel not found or you are not the owner."

        # Count the number of messages in the channel
        message_count = session.query(models.Wiadomosci).filter(models.Wiadomosci.kanal_odbiorcy == channel.id).count()

        session.close()
        return True, message_count  # Return the count of messages

    # operacja autoryzowana
    # channel_owner, channel identyfikuje tobie kanal
    # n - liczba ostatnich wiadomosci na kanale
    def get_channel_messages(self, channel_owner, channel_name, n):
        """Return the last n messages from the specified channel if the channel owner is valid."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        try:
            # Verify channel owner exists
            owner = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == channel_owner).first()
            if not owner:
                return False, "Channel owner not found."

            # Verify the channel exists
            channel = session.query(models.Kanaly).filter(
                models.Kanaly.nazwa_kanalu == channel_name,
                models.Kanaly.id_wlasciciela == owner.id
            ).first()

            if not channel:
                return False, "Channel not found or you are not the owner."

            # Fetch the last n messages associated with the channel
            messages = session.query(models.Wiadomosci).filter(models.Wiadomosci.kanal_odbiorcy == channel.id).order_by(models.Wiadomosci.data_wyslania.desc()).limit(n).all()

            if messages:
                return True, [(message.data_wyslania, message.nadawca_wiadomosci, message.zawartosc.decode('utf-8')) for message in messages]
            else:
                return False, "No messages found in this channel."

        except Exception as e:
            return False, f"Error occurred while fetching messages: {str(e)}"
        finally:
            session.close()  # Always close the session

    # operacja autoryzowana
    # channel_owner, channel identyfikuje tobie kanal
    def channel_delta(self, channel_owner, channel_name, timestamp):
        """Return all messages NEWER!!! than the given timestamp from the specified channel if the channel owner is valid."""
        Session = sessionmaker(bind=self.db_connection())
        session = Session()

        try:
            # Verify channel owner exists
            owner = session.query(models.Uzytkownicy).filter(models.Uzytkownicy.nazwa_uzytkownika == channel_owner).first()
            if not owner:
                return False, "Channel owner not found."

            # Verify the channel exists
            channel = session.query(models.Kanaly).filter(
                models.Kanaly.nazwa_kanalu == channel_name,
                models.Kanaly.id_wlasciciela == owner.id
            ).first()

            if not channel:
                return False, "Channel not found or you are not the owner."

            # Fetch messages newer than the specified timestamp
            messages = session.query(models.Wiadomosci).filter(
                models.Wiadomosci.kanal_odbiorcy == channel.id,
                models.Wiadomosci.data_wyslania > timestamp  # Compare against the provided timestamp
            ).order_by(models.Wiadomosci.data_wyslania.asc()).all()  # Order by sent date ascending

            if messages:
                return True, [(message.data_wyslania, message.nadawca_wiadomosci, message.zawartosc.decode('utf-8')) for message in messages]
            else:
                return False, "No new messages found in this channel."

        except Exception as e:
            return False, f"Error occurred while fetching new messages: {str(e)}"
        finally:
            session.close()  # Always close the session