# User Comment Management System

This project is a comprehensive user comment management system that allows user registration, login, and management of posts and comments. It features an automatic profanity and insult checking mechanism, comment analytics, and automated replies using AI.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Viewing the Database](#viewing-the-database)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Features

- **User Registration**: Allows users to create accounts and register.
- **User Login**: Secure login for registered users.
- **Post Management API**: Create, read, update, and delete posts.
- **Comment Management API**: Create, read, update, and delete comments.
- **Profanity Check**: Posts and comments are checked for profanity and insults during creation, and such entries are blocked.
- **Comment Analytics**: Get analytics on the number of comments added to posts over a specified period.
  - Example URL: `/api/comments-daily-breakdown?date_from=2020-02-02&date_to=2022-02-15`
  - Returns daily aggregated analytics, including the count of created and blocked comments.
- **Automatic Reply Function**: Users can enable automatic replies to comments on their posts, with a configurable delay and relevance to the content.

## Technologies Used

- **Backend Framework**: Django
- **Database**: SQLite, Django Ninja - Fast Django REST Framework
- **Asynchronous Task Queue**: Celery, Flower, Redis
- **Profanity Checking**: API Ninjas
- **AI for Comment Replies**: Gemini AI

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   
2. Navigate to the project directory:
   cd blog-service
   
3. Create a virtual environment (optional but recommended):
   python -m venv venv

4. Activate the virtual environment:
   -On Windows:
     venv\Scripts\activate
   -On macOS/Linux:
     source venv/bin/activate

5. Install the dependencies:
   pip install -r requirements.txt

6. Set up the database and apply migrations:
   python manage.py migrate

7. Run the development server:
   python manage.py runserver

8. Install Redis:
   - Download Redis from https://github.com/tporadowski/redis/releases.
   - Extract the downloaded archive.
   - Open the command prompt and navigate to the extracted Redis folder:
      cd path\to\redis-server.exe
   - Run Redis:
     redis-server.exe

9. In a new terminal, start the Celery worker:

   ```bash
   celery -A test_task worker --loglevel=INFO --pool=solo

10. (Optional) In another terminal, start the Flower server to monitor Celery tasks:
    celery ```bash -A test_task flower
    You can view the task dashboard at http://localhost:5555/.
    

## Viewing the Database

To view and manage the database through the Django admin panel, you need to create a superuser account.

### Steps to Create a Superuser

1. Run the following command in your terminal:
   ```bash
   python manage.py createsuperuser

2. Follow the prompts to enter your username, email, and password.

3. After creating the superuser, start the Django development server:
   python manage.py runserver

4. Access the Django admin panel by navigating to: http://127.0.0.1:8000/admin/
   
5. Log in with the superuser credentials you created, and you'll be able to view and manage the database.

## Usage

After setting up, you can access the API endpoints for managing posts and comments.
Use tools like Postman or cURL to interact with the APIs.
Ensure that you have configured your environment variables for any API keys required by API Ninjas and Gemini AI.

## API Endpoints

### Token Management
- **`POST /api/token/pair`**: Obtain Token
- **`POST /api/token/refresh`**: Refresh Token
- **`POST /api/token/verify`**: Verify Token

### User Management
- **`POST /api/register`**: Register a new user.
- **`POST /api/login`**: Log in a user.

### Comment Analytics
- **`GET /api/comments-daily-breakdown`**: Comments Daily Breakdown

### Post Management
- **`GET /api/posts`**: All Posts
- **`POST /api/posts`**: Create Post
- **`GET /api/posts/{post_id}`**: Post
- **`PUT /api/posts/{post_id}`**: Update Post
- **`DELETE /api/posts/{post_id}`**: Delete Post

### Comment Management
- `POST /api/create_comment`: Create a new comment.
  - **Note**: If the user has enabled the "Auto reply" feature, responses are generated using **Gemini AI**. However, **Gemini AI** is not supported in Ukraine, so you will need to use a VPN to enable this feature. 
  - To see the list of supported countries, visit [Gemini AI Supported Regions](https://ai.google.dev/gemini-api/docs/available-regions?hl=en).
- **`GET /api/comment/{post_id}`**: Get Comment
- **`PUT /api/comment/update/{comment_id}`**: Update Comment
- **`DELETE /api/comment/delete/{comment_id}`**: Delete Comment
- **`GET /api/users/{user_id}/comments`**: List Comments For User
