# # Where celery tasks are

# import os
# import time
# from celery import Celery


# celery = Celery(__name__)
# celery.conf.broker_url = os.environ.get(
#     "CELERY_BROKER_URL", "redis://localhost:6379")
# celery.conf.result_backend = os.environ.get(
#     "CELERY_RESULT_BACKEND", "redis://localhost:6379")


# @celery.task(name="send_sms_reminder")
# def send_sms_reminder(phone_number, reminder_text):
#     # Twilio sms code goes here
#     account_sid = os.environ['TWILIO_ACCOUNT_SID']
#     auth_token = os.environ['TWILIO_AUTH_TOKEN']
#     client = Client(account_sid, auth_token)

#     message = client.messages \
#                     .create(
#                         body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                         from_='+15017122661',
#                         to='+15558675310'
#                     )
#     print(phone_number)
#     print(reminder_text)
#     return True
