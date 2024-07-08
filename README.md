# My Reminder

My Reminder is a web application that allows users to set and manage reminders. It provides a simple interface for creating, editing, and deleting reminders, with email notifications sent on the specified date.

## Features

- Create reminders with custom messages and multiple email recipients
- Edit existing reminders
- Delete reminders
- View all reminders in a paginated list
- Automatic email notifications on the reminder date

## Technologies Used

- Backend: Flask (Python)
- Database: PostgreSQL
- Frontend: HTML, CSS (Tailwind CSS), JavaScript
- Email Service: Mailgun
- Containerization: Docker

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker and Docker Compose
- Python 3.7+
- pip (Python package manager)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/websim-reminders.git
   cd websim-reminders
   ```

2. Create a `.env` file in the project root directory with the following content:
   ```
   FLASK_APP=webapp.py
   FLASK_ENV=development
   FLASK_DEBUG=1

   # Database configuration
   DB_USER=user
   DB_PASSWORD=password
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=reminders

   # Mailgun configuration
   MAILGUN_API_KEY=your_mailgun_api_key
   MAILGUN_DOMAIN=your_mailgun_domain
   MAILGUN_SENDER=noreply@yourdomain.com

   # Secret key for Flask sessions
   SECRET_KEY=your_secret_key_here
   ```
   Replace the placeholder values with your actual configuration.

3. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

4. Initialize the database:
   ```
   docker-compose exec web flask init-db
   ```

5. The application should now be running at `http://localhost:5000`

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Click on "New Reminder" to create a new reminder
3. Fill in the date, message, and email address(es) for the reminder
4. Click "Save Reminder" to create the reminder
5. View all reminders on the home page
6. Double-click a reminder to edit or delete it

## Development

To run the application in development mode:

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Set up a local PostgreSQL database and update the `.env` file with the appropriate credentials

3. Run the Flask development server:
   ```
   flask run
   ```

4. The application will be available at `http://localhost:5000`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
