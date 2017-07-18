from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from flask_basicauth import BasicAuth
import os, dataset

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

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    #resp = MessagingResponse().message("Hello, Mobile Monkey")
    #return str(resp)
    return "passing for now!"

@app.route("/new", methods=['GET', 'POST'])
@basic_auth.required
def add_phone():
    """Respond to incoming calls with a simple text message."""
    db.create_table('users', primary_id='phone', primary_type="String")
    return "testing 1 2 3"

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
    return her

def acknowledge():
    pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)