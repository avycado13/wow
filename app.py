import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import time

import app.wow as wow

# Leave some room for the progress meter, like `(1/20) `
MESSAGE_SIZE = 1590

load_dotenv()

app = Flask(__name__)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# https://www.twilio.com/blog/receive-whatsapp-messages-python-flask-twilio
def respond(request, full_message):
    # Break the message up into chunks that fall under the WhatsApp character
    # limit and send them with a delay in between.
    chunks = (len(full_message) // MESSAGE_SIZE) + 1
    for i in range(chunks):
        start = i * MESSAGE_SIZE
        end = start + MESSAGE_SIZE
        progress = '({}/{}) '.format(i + 1, chunks)
        message_chunk = progress + full_message[start:end]
        client.messages.create(
            body=message_chunk,
            from_=request.form.get('To'),
            to=request.form.get('From'),
        )
        time.sleep(1)

    return str(MessagingResponse())


@app.route('/message', methods=['POST'])
def reply():
    message = request.form.get('Body')
    if message:
        if message.upper.startswith("GPT"):
            message = message.lower().replace("gpt", "")
            result = wow.get_assistant_response(message)
            return respond(request, result)
        result = wow.get_wiki_page(message)
        return respond(request, result)