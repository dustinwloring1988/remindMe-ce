from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
from sqlalchemy import desc
import logging
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(filename='reminders.log', level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
db = SQLAlchemy(app)

# Mailgun configuration
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
MAILGUN_SENDER = os.getenv('MAILGUN_SENDER')

# Check Mailgun configuration
if not MAILGUN_API_KEY:
    logging.error("MAILGUN_API_KEY is not set")
    print("Error: MAILGUN_API_KEY is not set")
if not MAILGUN_DOMAIN:
    logging.error("MAILGUN_DOMAIN is not set")
    print("Error: MAILGUN_DOMAIN is not set")

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    emails = db.Column(db.JSON, nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reminder')
@app.route('/reminder/<int:id>')
def reminder(id=None):
    return render_template('reminder.html', reminder_id=id)

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    
    reminders = Reminder.query.order_by(desc(Reminder.date)).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify([{
        'id': r.id,
        'date': r.date.isoformat(),
        'emails': r.emails,
        'message': r.message
    } for r in reminders.items]), 200

@app.route('/api/reminders/<int:id>', methods=['GET'])
def get_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    return jsonify({
        'id': reminder.id,
        'date': reminder.date.isoformat(),
        'emails': reminder.emails,
        'message': reminder.message
    }), 200

@app.route('/api/set-reminder', methods=['POST'])
def set_reminder():
    data = request.json
    reminder = Reminder(
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        emails=data['emails'],
        message=data['message']
    )
    db.session.add(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder set successfully!"}), 200

@app.route('/api/reminders/<int:id>', methods=['PUT'])
def update_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    data = request.json
    reminder.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    reminder.emails = data['emails']
    reminder.message = data['message']
    db.session.commit()
    return jsonify({"message": "Reminder updated successfully!"}), 200

@app.route('/api/reminders/<int:id>', methods=['DELETE'])
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder deleted successfully!"}), 200

def send_email(to, subject, body):
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={"from": MAILGUN_SENDER,
                  "to": to,
                  "subject": subject,
                  "text": body})
        
        response.raise_for_status()
        logging.info(f'Email sent successfully to {to}')
        print(f'Email sent successfully to {to}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to send email to {to}. Error: {str(e)}')
        print(f'Failed to send email to {to}. Error: {str(e)}')

def check_reminders():
    today = datetime.now().date()
    reminders = Reminder.query.filter_by(date=today).all()
    for reminder in reminders:
        for email in reminder.emails:
            try:
                send_email(email, "Here's Your Reminder", reminder.message)
                logging.info(f"Sent reminder to {email} for reminder id {reminder.id}")
            except Exception as e:
                logging.error(f"Failed to send reminder to {email} for reminder id {reminder.id}. Error: {str(e)}")
        db.session.delete(reminder)
    db.session.commit()
    logging.info(f"Reminder check completed. Processed {len(reminders)} reminders.")

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database tables created.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
