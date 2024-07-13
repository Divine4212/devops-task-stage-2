from flask import Flask, request
from mails import send_email, log_time

app = Flask(__name__)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    
    if sendmail:
        send_email.delay(sendmail)
        return f"Email queued to be sent to {sendmail}"
    
    if talktome:
        log_time.delay()
        return "Current time logged"
    
    return "Welcome to the messaging system"

if __name__ == '__main__':
#    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
