import celery
import os
import dataset
from twilio.rest import Client

# DATABASE
db = dataset.connect(os.environ['DATABASE_URL'])
table = db['users']

# TWILIO
account_sid = os.environ.get('TWILIO_SID')
auth_token = os.environ.get('TWILIO_AUTH')
client = Client(account_sid, auth_token)
phone = os.environ.get('TWILIO_PHONE')

# CELERY APP
app = celery.Celery('monica')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'], CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@app.task
def respond(number, old_state, new_state, message):
    print "responding asyncronisousfslfsaf to %s !!!: %s" % (number, message)
    # make sure there hasn't been a timeout
    user = table.find_one(phone=number)
    if user and user['state'] == old_state:
        data = {'phone':number, 'state':new_state}
        table.upsert(data, ['phone'])

        client.messages.create(
        to=number,
        from_=phone,
        body=message)
