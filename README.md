
# Django Chat Application

This is a simple Django-based chat application that allows users to create accounts, log in, view online users, start chats with online users, and send messages in real time. The project uses Django REST Framework for API functionality and Django Channels for WebSocket-based real-time communication.

## How to Run the Project

Follow these steps to run the Django Chat Application:

1. Clone the project repository to your local machine:

   ``` shell
   git clone https://github.com/inishantxchandel/django-chat-application.git
   ```

2. Navigate to the project directory:

   ``` shell
   cd chat_project
   ```

3. Create a virtual environment (optional but recommended):

   ```shell
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ``` shell
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ``` shell
     source venv/bin/activate
     ```

5. Install project dependencies:

   ```shell
   pip install -r requirements.txt
   ```

6. Apply database migrations:

   ```shell
   python manage.py migrate
   ```

The project should now be running locally. You can access the API endpoints using the provided URLs.

## Automated Testing

Automated testing is an essential part of the project to ensure that the application functions correctly. The project includes test cases for various API endpoints and functionality. To run the automated tests, follow these steps:

1. Make sure your virtual environment is activated.

2. Run the following command to execute the automated tests:

   ```shell
   python manage.py test
   ```

   This command will run the test cases and provide feedback on whether each test passed or failed.

## Testing with Postman

You can also test the API endpoints using Postman or any other API testing tool. Here are the available API endpoints and their functionality:

- **User Registration:**

  - Endpoint: `POST /api/register/`
  - Functionality: Allows users to create an account by providing a username, email, and password.

- **User Login:**

  - Endpoint: `POST /api/login/`
  - Functionality: Allows users to log in by providing their username or email and password.

- **User Logout:**

  - Endpoint: `POST /api/logout/`
  - Functionality: Allows users to log out.

- **Get Online Users:**

  - Endpoint: `GET /api/online-users/`
  - Functionality: Retrieves a list of all online users who are currently available for chat.

- **Start a Chat:**

  - Endpoint: `POST /api/chat/start/`
  - Functionality: Allows a user to initiate a chat with another online user.

- **Send a Message:**

  - Endpoint: `POST /api/chat/send/`
  - Functionality: Allows a user to send and receive instant messages to/from another online user in real-time.

- **Recommended Friends:**

  - Endpoint: `GET /api/suggested-friends/<user_id>/`
  - Functionality: Returns the top 5 recommended friends for the specified user based on a recommendation algorithm.

Make sure to include the appropriate request headers for authentication (e.g., using tokens) when testing the endpoints that require authentication.

## Implemented Views and Their URLs

- User Registration: `POST /api/register/`
- User Login: `POST /api/login/`
- User Logout: `POST /api/logout/`
- Get Online Users: `GET /api/online-users/`
- Start a Chat: `POST /api/chat/start/`
- Send a Message: `WEBSOCKET /api/chat/send/`
- Recommended Friends: `GET /api/suggested-friends/<user_id>/`
