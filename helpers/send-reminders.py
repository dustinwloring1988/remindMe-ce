import sys
import os
import logging

# Set up logging
logging.basicConfig(filename='reminders.log', level=logging.INFO)

# Add the directory containing your webapp.py to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from webapp import app, db, check_reminders

    # Create an application context
    with app.app_context():
        # Run the check_reminders function
        check_reminders()

    print("Reminders checked and sent.")
    logging.info("Reminders checked and sent successfully.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    logging.error(f"An error occurred while checking reminders: {str(e)}")

