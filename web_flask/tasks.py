from models.Base_mode import Exerciseplan
from datetime import datetime, time, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery

celery = Celery(__name__)

@celery.task
def send_exercise_reminders():
    # Get current time
    now = datetime.now().time()

    # Get exercise plans whose exercise time is within 15 minutes of current time
    exercise_plans = Exerciseplan.query.filter(Exerciseplan.exercise_time.between(
        (datetime.combine(datetime.today(), now).time()),
        (datetime.combine(datetime.today(), now).time()) + timedelta(minutes=15)
    )).all()

    # Send reminders for exercise plans
    for exercise_plan in exercise_plans:
        # Send reminder via email, SMS, or push notification
        send_email(exercise_plan.user.email, 'Exercise Reminder', f"Don't forget to do {exercise_plan.name} at {exercise_plan.exercise_time}")

def send_email(email, subject, message):
    # Code to send email using a library like smtplib or a third-party service like SendGrid
    # Example using smtplib:

    # Set up the email content
    msg = MIMEMultipart()
    msg['From'] = 'gershommethod02@gmail.com'
    msg['To'] = email
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.send_message(msg)
