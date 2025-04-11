# Doctor Appointment Management System

A Django-based doctor appointment system with SMS notifications.

## Features

- User authentication
- Doctor appointment scheduling
- SMS notifications for password reset
- Admin dashboard
- Doctor dashboard
- Patient dashboard

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

4. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Twilio Setup

1. Sign up for a Twilio account at https://www.twilio.com
2. Get your Account SID and Auth Token from the Twilio Console
3. Get a Twilio phone number
4. Update the .env file with your Twilio credentials

## Database Setup

1. Create a MySQL database named 'docaspythondb'
2. Update the database settings in settings.py if needed

## Testing SMS

Visit http://127.0.0.1:8000/test-notifications/ to test the SMS functionality. 