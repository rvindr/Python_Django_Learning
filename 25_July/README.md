# Expense Tracker

## Overview

Expense Tracker is a Django-based web application designed to help users manage and track their expenses. It features user authentication with signup, login, and logout functionalities. The project uses SQLite as its default database and Pillow for image handling.

## Features

- **User Authentication**: Allows users to sign up, log in, and log out.
- **Expense Tracking**: Users can manage and track their expenses.

## Setup Instructions
### 1. Clone the Repository:
Open your terminal and run:
```bash
git clone https://github.com/rvindr/expense_tracker_django.git
```

### 2. Create and Activate Virtual Environment

Create a virtual environment and activate it:

```bash
python -m venv env
source env/bin/activate
```
### 3. Install Dependencies
Install the required packages:
```bash
pip install django
pip install pillow
```
### 4. Apply Migrations
Navigate to the project directory and apply migrations:
```bash
cd expense
python manage.py makemigrations
python manage.py migrate
```
### 5. Run the Application
Start the development server:
```bash
python manage.py runserver
```
Access the admin panel at http://127.0.0.1:8000/admin/

### Screenshots
Here are some screenshots of the application:
<img width="1440" alt="Screenshot 2024-07-25 at 5 25 31 PM" src="https://github.com/user-attachments/assets/d4fea40b-3123-46bc-afff-91ceb4c9525b">
<img width="1440" alt="Screenshot 2024-07-25 at 5 25 42 PM" src="https://github.com/user-attachments/assets/09c83c6c-445c-47b9-b34c-2a98ff04fc79">
<img width="1440" alt="Screenshot 2024-07-25 at 5 26 01 PM" src="https://github.com/user-attachments/assets/acde697e-c241-476e-af51-123f7c3c10e4">


### Contributing
Feel free to fork the repository and submit pull requests. For any issues or feature requests, please open an issue on GitHub.




