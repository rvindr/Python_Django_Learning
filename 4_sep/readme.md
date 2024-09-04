# Celery and Redis Integration with Django

This project demonstrates how to integrate Celery with Redis in a Django application to handle asynchronous tasks.

## Installation

Before you begin, make sure you have the following installed:

1. **Redis**: Make sure Redis is installed on your machine.
2. **Celery**: Install Celery and Redis Python packages:

   ```bash
   pip install redis
   pip install celery
   ```

## Setup

1. **Create `celeryDemo/celery.py` file**: 

   In your project folder (where `settings.py` resides), create a file named `celery.py`.

2. **Configure Celery**:

   Paste the necessary configuration into your `celeryDemo/__init__.py` file. You can refer to the Celery documentation for details or use the following code:

   ```python
   from .celery import app as celery_app

    __all__ = ('celery_app',)
   ```

3. **Update Django Settings**:

   Add the following Celery-related settings to your `settings.py` file:

   ```python
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TASK_SERIALIZER = 'json'
   CELERY_RESULT_SERIALIZER = 'json'
   CELERY_TIMEZONE = 'UTC'
   ```

4. **Create `home/tasks.py` file**:

   In your Django app folder, create a file named `tasks.py`. This is where you will define your asynchronous tasks.

5. **Write Tasks**:

   Define your tasks in `tasks.py` using Celery. For example:

   ```python
   from celery import shared_task

   @shared_task
   def add(x, y):
       return x + y
   ```

6. **Use Tasks in Views**:

   To execute the tasks, call them from your `views.py`. Instead of directly calling the function, use the `delay` method:

   ```python
   def index(request):
    result = add.delay(10,5)
    return render(request, 'index.html',context={'data':'here is the demo text'})
   ```

## Running the Project

1. **Start the Celery Worker**:

   Open a terminal and navigate to your project directory. Start the Celery worker with the following command:

   ```bash
   celery -A celeryDemo worker -l info
   ```

2. **Run the Django Server**:

   In another terminal, run the Django development server:

   ```bash
   python manage.py runserver
   ```

