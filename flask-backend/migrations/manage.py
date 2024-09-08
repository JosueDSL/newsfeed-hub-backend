# Description: This file is used to manage the database migrations.

# Import the required modules
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app, db

# Create an instance of the Flask application
app = create_app()
with app.app_context():     # Run the manager in the application context
    manager = Manager(app)

# Add the 'db' command to the manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()