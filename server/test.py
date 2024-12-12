import database as db
import datetime

db = db.Database()


# New user addition - non existing user
result, message = db.sign_up_user('new_username22', 'new_email2@example.com', 'securepassword1226')
print(f'Case 1: {message}')

# New user addition - email already used
result, message = db.sign_up_user('new_username21', 'new_email1@example.com', 'securepassword11')
print(f'Case 2: {message}')

# New user addition - existing user handler
result, message = db.sign_up_user('new_username2', 'new_email12@example.com', 'securepassword12123')
print(f'Case 3: {message}')

# Verification test case - correct validation:
result, message = db.check_credentials('new_username22', 'securepassword1226')
print(f'Case 4: {message}')

# Verification test case - incorrect user:
result, message = db.check_credentials('new_username23', 'securepassword1226')
print(f'Case 5: {message}')

# Verification test case - incorrect both:
result, message = db.check_credentials('new_username23', 'securepassword1212333')
print(f'Case 6: {message}')

# New channel addition - existing channel handler
result, message = db.create_channel('new_username22', 'channel_1', ['new_username21', 'new_username22'])
print(f'Case 7: {message}')

# New channel addition - lack of exisiting user
result, message = db.create_channel('new_username23', 'channel_4', ['new_username', 'new_username23', 'newusername29'])
print(f'Case 8: {message}')

# List channels for this user
result, message_or_channels = db.list_channels('new_username22')

if result:
    print("Case 9: channels:", message_or_channels)  # Print the list of channels
else:
    print("Case 9: error:", message_or_channels)  # Print the error message

# New channel addition - test before removal
result, message = db.create_channel('new_username22', 'test_channel', ['new_username21', 'new_username22'])
print(f'Case 7: {message}')

# Remove the channel - channel exists and user is an owner
result, message = db.remove_channel('new_username22', 'test_channel')
print(f'Case 10: {message}')

# Remove the channel - channel does not exist and user is an owner
result, message = db.remove_channel('new_username22', 'channel_12')
print(f'Case 11: {message}')

# New channel addition - lack of exisiting user
result, message = db.create_channel('new_username28', 'channel_1', ['new_username21', 'new_username22', 'new_username28'])
print(f'Case 12: {message}')

# Add channel member - success
result, message = db.add_channel_member('new_username22', 'channel_1', 'new_username2')
print(f'Case 13: {message}')


# Remove user from teh channel

result, message = db.remove_channel_member('new_username22', 'channel_1', 'new_username21')
print(f'Case 14: {message}')

# Send a message to the channel
result, message = db.send_message('new_username22', 'channel_1', 'Hello, everyone!')
print(f'Case 15: {message}')

# Send a message to the channel that does not exist
result, message = db.send_message('new_username22', 'channel_24', 'Hello, everyone!')
print(f'Case 16: {message}')

# Send a message to the channel that user is not a part of
result, message = db.send_message('new_username21', 'channel_2', 'Hello, everyone!')
print(f'Case 17: {message}')

# Number of messages in a channel

result, message_or_count = db.channel_length('new_username22', 'channel_1')  # Correct method call
if result:
    print(f"Case 18: number of messages in channel: {message_or_count}")
else:
    print(f'Case 18: {message_or_count}')  # Error message

# Example of get_channel_messages function
result, messages_or_message = db.get_channel_messages('new_username22', 'channel_1', 4)

# Output the result or error message
if result:
    print("Messages:", messages_or_message)  # List of messages
else:
    print("Error:", messages_or_message)  # Error message

# Example of the delta function - returns messsages newer than the timestamp
timestamp = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)  # Example: 5 minutes ago
result, messages_or_message = db.channel_delta('new_username22', 'channel_1', timestamp)

if result:
    print("New Messages:", messages_or_message)
else:
    print("Error:", messages_or_message)