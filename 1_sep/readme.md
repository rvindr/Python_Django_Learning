#django-crontab


# Django Cron Job Setup Guide

This guide provides step-by-step instructions for setting up a cron job that runs every minute in a Django project using the `django-crontab` package.

## Prerequisites

Before proceeding, ensure you have the following:

- **Python** and **Django** installed in your environment.
- Basic understanding of Django project structure and Python programming.

## Step 1: Install `django-crontab`

To begin, you need to install the `django-crontab` package. This package allows you to easily manage cron jobs within your Django project.

Use the following command to install `django-crontab`:

```bash
pip install django-crontab
```

## Step 2: Add `django-crontab` to Installed Apps

Next, you need to add `django-crontab` to the `INSTALLED_APPS` section of your `settings.py` file.

Open `settings.py` and add `django_crontab` like so:

```python
# settings.py

INSTALLED_APPS = [
    ...
    'django_crontab',
    ...
]
```

## Step 3: Define the Cron Job

Now, you will define the cron job in your `settings.py` file. The cron job will be configured to run every minute.

Add the following code to `settings.py`:

```python
# settings.py

CRONJOBS = [
    ('* * * * *', 'yourapp.cron.my_scheduled_job'),
]
```

- The cron expression `* * * * *` indicates that the job will run every minute.
- Replace `yourapp.cron.my_scheduled_job` with the correct path to the function you want to run.

## Step 4: Create the Cron Job Function

Create a `cron.py` file inside your Django app directory. This file will contain the function that will be executed by the cron job.

For example, if your app is named `yourapp`, create `yourapp/cron.py` and add the following content:

```python
# yourapp/cron.py

def my_scheduled_job():
    # Your scheduled task here
    print("This job runs every minute")
```

This function will be executed every minute by the cron job.

## Step 5: Apply the Cron Job

To apply the cron job to your system's crontab, run the following management command:

```bash
python manage.py crontab add
```

This command will add the cron job defined in `settings.py` to your system's crontab.

## Step 6: Manage Cron Jobs

You can manage your cron jobs using the following commands:

- **List active cron jobs:**

  ```bash
  python manage.py crontab show
  ```

- **Remove a cron job:**

  ```bash
  python manage.py crontab remove
  ```

## Step 7: Verify the Cron Job

To verify that your cron job is working, you can either:

- Check the console output for the message "This job runs every minute" if you are running the Django server.
- Check system logs to confirm that the cron job is being executed.

