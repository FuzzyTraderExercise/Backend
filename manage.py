from flask.cli import FlaskGroup
from src import create_app, db

app = create_app()

cli = FlaskGroup(create_app=create_app)

# Run Flask
if __name__ == '__main__':
    cli()