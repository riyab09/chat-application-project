ChatApp
Description
ChatApp is a real-time messaging application built using Django and Channels. Users can join different chat rooms and send/receive messages instantly through WebSockets.

Prerequisites
Before running the project, you need to have the following:

Python 3.x (preferably Python 3.8 or higher)
Redis (used for WebSocket message handling)
Django (web framework)
Channels (for handling WebSockets)
Steps to Run ChatApp Project
1. Clone the Repository

git clone https://github.com/your-username/chatapp.git
cd chatapp

2.Create a Virtual Environment

python -m venv venv

3.the Virtual Environment


.\venv\Scripts\activate  # For Windows

4.Install Dependencies

pip install -r requirements.txt

5. Install and Start Redis (Memurai)

Download Memurai from here.

Start Memurai:


"C:\Program Files\Memurai\memurai-server.exe"

6.Run Migrations

python manage.py migrate

7.Run the Server

python manage.py runserver

8.Access the Application

Open your browser and go to:


http://127.0.0.1:8000/

9.Test the Chat Functionality

Go to http://127.0.0.1:8000/chat/room_name/ to join any chat room.
Open the chat room in multiple tabs to test real-time messaging.
