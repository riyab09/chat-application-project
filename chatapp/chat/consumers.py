# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth.models import User
# from .models import Message
# from asgiref.sync import sync_to_async


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         user1 = self.scope['user'].username 
#         user2 = self.room_name
#         self.room_group_name = f"chat_{''.join(sorted([user1, user2]))}"

#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = self.scope['user']  
#         receiver = await self.get_receiver_user() 

#         await self.save_message(sender, receiver, message)

#         await self.channel_layer.group_send(
#             self.room_group_name,
            
#             {
#                 'type': 'chat_message',
#                 'sender': sender.username,
#                 'receiver': receiver.username,
#                 'message': message
#             }
#         )
        

#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']
#         receiver = event['receiver']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'sender': sender,
#             'receiver': receiver,
#             'message': message
#         }))

#     @sync_to_async
#     def save_message(self, sender, receiver, message):
#         Message.objects.create(sender=sender, receiver=receiver, content=message)

#     @sync_to_async
#     def get_receiver_user(self):
#         return User.objects.get(username=self.room_name)

# //////////////////////////////////////////////

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from chat.models import Message
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User
# import logging

# logger = logging.getLogger(__name__)


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = text_data_json['username']
#         sender_username = text_data_json.get('sender_username')  # Adjust according to your message format
#         logger.debug(f"Received message: {text_data_json}")  # Add this line for debugging
      

#         if not sender_username:
#            logger.error("sender_username is missing in the message!")
#            return
#         sender_exists = await database_sync_to_async(User.objects.filter(username=sender_username).exists)()
#         if not sender_exists:
#            logger.error(f"User {sender_username} not found!")
#            await self.send(text_data=json.dumps({
#             'error': 'User not found'
#           }))
#         return
#         if sender_username:
#             try:
#                 sender = await database_sync_to_async(User.objects.get)(username=sender_username)
#             except User.DoesNotExist:
#             # Handle the case when the user does not exist
#               print(f"User {sender_username} not found!")
#             # Optionally send a message back to the WebSocket client
#             await self.send(text_data=json.dumps({
#                 'error': 'User not found'
#             }))
#             return
#         room_name = text_data_json['room_name']
#         sender = await database_sync_to_async(User.objects.get)(username=sender_username)
#         # Save message to database
#         await database_sync_to_async(self.save_message)(sender, room_name, message)
        
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender_username': sender_username,
#             }
#         )
#     # except Exception as e:
#     #     logger.exception("Error in WebSocket receive method:", exc_info=e)
#     #     await self.send(text_data=json.dumps({
#     #             'error': 'An error occurred while processing your message.'
#     #         }))


#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         sender_username = event['sender']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender_username': sender,
#         }))

#     def save_message(self, sender, room_name, message):
#         # Save message to the database
#         Message.objects.create(
#             sender=sender,
#             receiver=room_name,
#             content=message,
#         )
    
#     def get_user_by_username(username):
#         """
#         Retrieve a User instance by username.
#         """
#         try:
#             return User.objects.get(username=username)
#         except User.DoesNotExist:
#             return None
        
        
# import json
# import logging
# from channels.generic.websocket import AsyncWebsocketConsumer
# from chat.models import Message
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User

# logger = logging.getLogger(__name__)

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         # Join the room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

    # async def receive(self, text_data):
    #     try:
    #         text_data_json = json.loads(text_data)
    #         message = text_data_json.get('message')
    #         sender_username = text_data_json.get('sender_username')
    #         room_name = text_data_json.get('room_name')

    #         logger.debug(f"Received message: {text_data_json}")

    #         # Validate required fields
        #     if not all([message, sender_username, room_name]):
        #         logger.error("Missing required fields in the message!")
        #         await self.send(text_data=json.dumps({
        #             'error': 'Required fields (message, sender_username, room_name) are missing.'
        #         }))
        #         return

        #     # Check if the sender exists
        #     sender = await database_sync_to_async(self.get_user_by_username)(sender_username)
        #     if not sender:
        #         logger.error(f"User {sender_username} not found!")
        #         await self.send(text_data=json.dumps({
        #             'error': f'User {sender_username} not found.'
        #         }))
        #         return

        #     # Save the message to the database
        #     await database_sync_to_async(self.save_message)(sender, room_name, message)

        #     # Broadcast the message to the room group
        #     await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type': 'chat_message',
        #             'message': message,
        #             'sender_username': sender_username,
        #         }
        #     )
        # except Exception as e:
        #     logger.exception("Error in WebSocket receive method:", exc_info=e)
        #     await self.send(text_data=json.dumps({
        #         'error': 'An error occurred while processing your message.'
        #     }))
    #     if not message or not sender_username or not room_name:
    #         logger.error("Missing required fields: message, sender_username, or room_name.")
    #         await self.send(text_data=json.dumps({
    #             'error': 'Required fields (message, sender_username, room_name) are missing.'
    #         }))
    #         return

    #     # Check if the sender exists in the database
    #     try:
    #         sender = await database_sync_to_async(User.objects.get)(username=sender_username)
    #     except User.DoesNotExist:
    #         logger.error(f"User {sender_username} not found.")
    #         await self.send(text_data=json.dumps({
    #             'error': 'User does not exist.'
    #         }))
    #         return

    #     # Save the message to the database
    #     await database_sync_to_async(self.save_message)(sender, room_name, message)

    #     # Send the message to the room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message,
    #             'sender': sender_username,  # Send the username of the sender
    #         }
    #     )

    # #   except Exception as e:
    # #     logger.exception("An error occurred in the WebSocket receive method:", exc_info=e)
    # #     await self.send(text_data=json.dumps({
    # #         'error': 'An internal error occurred. Please try again later.'
    # #     }))
    # # async def receive(self, text_data):
    # #     try:
    # #     # Parse the incoming JSON message
    # #       text_data_json = json.loads(text_data)
    # #       logger.debug(f"Received message data: {text_data_json}")

    # #     # Extract message, sender_username, and room_name from the incoming JSON
    # #       message = text_data_json.get('message')
    # #       sender_username = text_data_json.get('sender_username')
    # #       room_name = text_data_json.get('room_name')

    # #     # Check if any required field is missing
    # #       if not message or not sender_username or not room_name:
    # #         logger.error("Missing required fields: message, sender_username, or room_name.")
    # #         await self.send(text_data=json.dumps({
    # #             'error': 'Required fields (message, sender_username, room_name) are missing.'
    # #         }))
    # #         return

    # #     # Check if the sender exists in the database
    # #     try:
    # #         sender = await database_sync_to_async(User.objects.get)(username=sender_username)
    # #     except User.DoesNotExist:
    # #         logger.error(f"User {sender_username} not found.")
    # #         await self.send(text_data=json.dumps({
    # #             'error': 'User does not exist.'
    # #         }))
    # #         return

    # #     # Save the message to the database
    # #     await database_sync_to_async(self.save_message)(sender, room_name, message)

    # #     # Send the message to the room group
    # #     await self.channel_layer.group_send(
    # #         self.room_group_name,
    # #         {
    # #             'type': 'chat_message',
    # #             'message': message,
    # #             'sender': sender_username,  # Send the username of the sender
    # #         }
    # #     )

    # #     except Exception as e:
    # #     logger.exception("An error occurred in the WebSocket receive method:", exc_info=e)
    # #     await self.send(text_data=json.dumps({
    # #         'error': 'An internal error occurred. Please try again later.'
    # #     }))


    # async def chat_message(self, event):
    #     # Handle messages sent to the room group
    #     message = event['message']
    #     sender_username = event['sender_username']

    #     # Send the message to the WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         'sender_username': sender_username,
    #     }))

    # @staticmethod
    # def save_message(sender, room_name, message):
    #     """
    #     Save a message to the database.
    #     """
    #     Message.objects.create(
    #         sender=sender,
    #         receiver=room_name,  # Update this if your model uses different fields
    #         content=message,
    #     )

    # @staticmethod
    # def get_user_by_username(username):
    #     """
    #     Retrieve a User instance by username.
    #     """
    #     try:
    #         return User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return None


import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # async def receive(self, text_data):
    #     try:
    # #         # Parse the incoming JSON message
    #         text_data_json = json.loads(text_data)
    #         logger.debug(f"Received message: {text_data_json}")

    #         # Extract the necessary fields from the message
    #         message = text_data_json.get('message')
    #         sender_username = text_data_json.get('sender_username')
    #         room_name = text_data_json.get('room_name')

    #         # Validate required fields
    #         if not all([message, sender_username, room_name]):
    #             logger.error("Missing required fields: message, sender_username, or room_name.")
    #             await self.send(text_data=json.dumps({
    #                 'error': 'Required fields (message, sender_username, room_name) are missing.'
    #             }))
    #             return

    #         # Check if the sender exists in the database
    #         sender = await database_sync_to_async(User.objects.get)(username=sender_username)
    #     except User.DoesNotExist:
    #         logger.error(f"User {sender_username} not found.")
    #         await self.send(text_data=json.dumps({
    #             'error': f'User {sender_username} not found.'
    #         }))
    #         return
    #     except Exception as e:
    #         logger.error(f"Error occurred: {str(e)}")
    #         await self.send(text_data=json.dumps({
    #             'error': 'An error occurred while processing your message.'
    #         }))
    #         return
async def receive(self, text_data):
    try:
        logger.debug(f"Raw data received: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender_username = text_data_json.get('sender_username')
        room_name = text_data_json.get('room_name')
        logger.debug(f"Parsed data: message={message}, sender={sender_username}, room={room_name}")

        # Validate and handle logic here...

    except Exception as e:
        logger.error(f"Error in receive: {e}")


        # Save the message to the database
        await database_sync_to_async(self.save_message)(sender, room_name, message)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username,  # Send the username of the sender
            }
        )

    async def chat_message(self, event):
        # Handle messages sent to the room group
        message = event['message']
        sender_username = event['sender_username']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_username': sender_username,
        }))

    @staticmethod
    def save_message(sender, room_name, message):
        """
        Save a message to the database.
        """
        Message.objects.create(
            sender=sender,
            receiver=room_name,  # Update this if your model uses different fields
            content=message,
        )
async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'chat_{self.room_name}'

    logger.info(f"WebSocket connection request for room: {self.room_name}")

    # Join room group
    await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
    )
    await self.accept()
    logger.info(f"WebSocket connection established for room: {self.room_name}")
