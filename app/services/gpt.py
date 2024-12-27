from openai import OpenAI
from flask import current_app

def get_openai_client():
    return OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

def get_assistant_response(user_input:str):
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
    )
    assistant_response = response.choices[0].message
    return assistant_response