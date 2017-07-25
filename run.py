from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask_basicauth import BasicAuth
import os, dataset, tasks

##################
# INITIALIZE APP #
##################

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('USER')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('PASS')

basic_auth = BasicAuth(app)

#################
# INITIALIZE DB #
#################

db = dataset.connect(os.environ['DATABASE_URL'])
table = db['users']

#####################
# INITIALIZE TWILIO #
#####################

account_sid = os.environ.get('TWILIO_SID')
auth_token = os.environ.get('TWILIO_AUTH')
client = Client(account_sid, auth_token)
phone = os.environ.get('TWILIO_PHONE')

@app.route("/", methods=['GET', 'POST'])
def discuss():
    body = request.values.get('Body', None)
    from_number = request.values.get('From')
    print from_number
    response = ""
    # MAKE SURE USER IS INCLUDED
    user = table.find_one(phone=from_number)
    if user:
        print user
        question = is_question(body)
        state = user['stage']
        if state == 'where_were_u':
            if question:
                (new_state, response) = formulate_answer(body)
                update_state(user, new_state)
            else:
                response = monica(body, 2)
                update_state(user, "monica_2")
                # state should be monica_2
        elif state == 'monica':
            pass
        elif state == 'monica_2':
            if question:
                (state, response) = formulate_answer(body)
            else:
                response = monica(body, 5)
        elif state == 'monica_5':
            pass
        elif state == 'come_on':
            pass
        elif state == 'why_the_q':
            pass
        elif state == 'u_like_that':
            pass
        elif state == 'srsly':
            tasks.respond.apply_async((from_number, state, 'where_were_u', 'where where u', table), countdown=25)
    resp = MessagingResponse()
    resp.message(response)
    print response
    print str(resp)
    return str(resp)

@app.route("/new", methods=['GET', 'POST'])
@basic_auth.required
def add_phone():
    """Respond to incoming calls with a simple text message."""
    if request.method == 'POST':
        phone = "%s%s%s" % (request.form['area'], request.form['first'], request.form['last'])
        if all(c.isdigit() for c in phone):
            data = dict([
                ("phone", "+1%s" % phone),
                ("name", request.form['name']),
                ("stage", "where_were_u"),
            ])
            table.upsert(data, ['phone'])
            return render_template('addeduser.html', title="congrats!", dialog="you successfully added a user. we're all very proud.")
        else:
            return render_template('addeduser.html', title="uhhh", dialog="not a real number. <a href='https://oh-monica.herokuapp.com/new'>try again?</a>")
    else:
        return render_template('addnumber.html')

@app.route("/whomst", methods=['GET'])
@basic_auth.required
def whomst():
    users = []
    for row in table.all():
        users.append(row)

    return render_template('whomst.html', users=users)

def update_state(user, state):
    data = { 'phone': user['phone'], 'state': state }
    table.upsert(data, ['phone'])
    return True

def formulate_answer(body):
    if body.lower.startswith('who'):
        return ("monica", "monica!")
    else:
        question_body = ""
        response = "Why the %s?" % question_body
        return ("why_the_q", response)

def is_question(body):
    content = body.lower()
    if content.endswith("?") \
    or content.startswith("who") \
    or content.startswith('what') \
    or content.startswith('wat') \
    or content.startswith("why") \
    or content.startswith('where') \
    or content.startswith('when'):
        return True
    else:
        return False

def monica(src, maxletters=None):
    tome = {
        97: "yes",
        98: "like this?",
        99: "tell me,",
        100: "teach me,",
        101: "yes",
        102: "shape me,",
        103: "sir",
        104: "as you like,",
        105: "yes",
        106: "this right?",
        107: "like that?",
        108: "go on",
        109: "show me,",
        110: "please sir",
        111: "yes",
        112: "god",
        113: "in here?",
        114: "oh sir",
        115: "so good",
        116: "you like that?",
        117: "yes",
        118: "in there?",
        119: "Jesus",
        120: "that right?",
        121: "god yes,",
        122: "in there?",
        65: "I need it,",
        66: "I know,",
        67: "I want it,",
        68: "Mister",
        69: "I deserve it,",
        70: "I need it,",
        71: "my god",
        72: "I am yours,",
        73: "I need it,",
        74: "I know,",
        75: "I deserve it,",
        76: "Mother",
        77: "teacher",
        78: "I am yours,",
        79: "I want it,",
        80: "I need it,",
        81: "I know,",
        82: "preacher",
        83: "I need it,",
        84: "I deserve it,",
        85: "I want it,",
        86: "I need it,",
        87: "Father",
        88: "my dear",
        89: "I deserve it,",
        90: "senator",
        44: "more sir,",
        45: "go on sir,",
        48: 'lower?',
        49: "more?",
        50: "louder?",
        51: "wider?",
        52: "tighter?",
        54: "looser?",
        55: "wetter?",
        56: "again?",
        57: "faster?",
        58: "slower?",
    }
    her = []
    acceptable = ''.join(c for c in src if tome.get(ord(c)))
    for c in acceptable[:maxletters]:
        call = tome.get(ord(c))
        her.append(call)
    return " ".join(her)

def acknowledge():
    pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)