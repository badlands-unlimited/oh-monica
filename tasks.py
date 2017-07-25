import celery
import os
from twilio.rest import Client

# TWILIO
account_sid = os.environ.get('TWILIO_SID')
auth_token = os.environ.get('TWILIO_AUTH')
client = Client(account_sid, auth_token)
phone = os.environ.get('TWILIO_PHONE')

# CELERY APP
app = celery.Celery('monica')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'], CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@app.task
def respond(number, old_state, new_state, message, table):
    # make sure there hasn't been a timeout
    user = table.find_one(number=number)
    if user and user['state'] == old_state:
        data = {'number':number, 'state':new_state}
        table.upsert(data, ['number'])

        client.messages.create(
        to=number,
        from_=phone,
        body=message)

