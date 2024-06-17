# app.py

from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import cohere
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

COHERE_API_KEY = 'X3CYRdttly6iEKBa3VrFYubKYp5JTJJvQmcAJu6R'
cohere_client = cohere.Client(COHERE_API_KEY)

class ChatForm(FlaskForm):
    user_input = StringField('You:', validators=[DataRequired()])
    submit = SubmitField('Send')

@app.route('/', methods=['GET', 'POST'])
def chat():
    form = ChatForm()
    if 'chat_history' not in session:
        session['chat_history'] = []
    bot_response = ""
    if form.validate_on_submit():
        user_input = form.user_input.data
        if not user_input.strip():
            bot_response = "Please enter a valid input."
        else:
            session['chat_history'].append(f"You: {user_input}")
            try:
                bot_response = get_bot_response(session['chat_history'])
                session['chat_history'].append(f"Bot: {bot_response}")
            except Exception as e:
                bot_response = f"An error occurred: {e}"
    return render_template('home.html', form=form, output=bot_response, chat_history=session['chat_history'])

def get_bot_response(chat_history):
    prompt = "\n".join(chat_history) + "\nBot:"
    response = cohere_client.generate(
        model='command',
        prompt=prompt,
        max_tokens=50,
        stop_sequences=["You:"]
    )
    return response.generations[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)
