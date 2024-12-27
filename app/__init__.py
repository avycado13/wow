import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import time
from .handlers.registry import HandlerRegistry
from config import Config

from app.services import get_assistant_response,get_wikipedia_content

# Leave some room for the progress meter, like `(1/20) `
MESSAGE_SIZE = 1590


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    client = Client(app.config["TWILIO_ACCOUNT_SID"], app.config["TWILIO_AUTH_TOKEN"])
    handler_registry = HandlerRegistry()

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
            handler = handler_registry.get_handler(message)
            result = handler.handle(message)
            return respond(request, result)
        return str(MessagingResponse())
    return app