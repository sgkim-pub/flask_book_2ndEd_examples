from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'YOUR_ACCOUNT'
app.config['MAIL_PASSWORD'] = 'YOUR_PASSWORD'

mail = Mail(app)

@app.route("/")
@app.route("/home")
def home():
    msg = Message(subject='Hello Flask Mail', sender='noreply@abc.com', recipients=['수신자 이메일 주소'])
    msg.body = f'Hello, this email is sent using Flask Mail:)'
    mail.send(msg)
    return "A test email is sent"

if __name__ == '__main__':
    app.run("127.0.0.1", 5000)