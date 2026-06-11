import os
import click
from src import create_app, db

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Determine the environment and configure the app
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

# Create the Flask application instance
app = create_app(FLASK_ENV)


@app.cli.command('create-db')
@click.option('--drop', is_flag=True, help='Drop existing tables before creating new ones.')
def create_db_command(drop):
    """Initializes or resets the database."""
    if drop:
        click.confirm('This will delete all data. Are you sure?', abort=True)
        db.drop_all()
        click.echo('Dropped all tables.')
    db.create_all()
    click.echo('Initialized the database.')


if __name__ == '__main__':
    app.run()
