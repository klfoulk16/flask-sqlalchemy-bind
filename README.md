# Flask SQLAlchemy Bind

Minimalistic extension to add support for SQLAlchemy to your Flask app. Adds most essential functionality - the database table construction is still be figured out.

## Set Up:
Install using pip:
```bash
pip install flask-sqlalchemy-bind
```

## A Simple Flask App

A simple Flask app steup using Flask-SQLAlchemy-Bind:
```python
    from flask import Flask
    from flask_sqlalchemy_bind import SQLAlchemy

    app = Flask(__name__)
    app.config["DATABASE"] = "sqlite:///:memory:"
    db = SQLAlchemy(app)

    from sqlalchemy import Column, Integer, String
    class User(db.Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)
        password = Column(String, unique=True)

        def __init__(self, username=None, password=None):
            self.username = username
            self.password = password

    db.session.add(User(username="Hi", email="itsme@example.com"))
    db.session.commit()

    users = User.query.all()
```

## Adding a Click Command to Reset the Database

If you'd like to add a command line tool to reset the database add the following code to the your application:

```python
import click
from flask.cli import with_appcontext

# create convenient click command for resetting database
@click.command('reset-db')
@with_appcontext
def reset_db_command():
    """Clear the existing data and create new tables."""
    db.empty_db()
    db.init_db()
    click.echo('Reset the database.')
```

Using the new CLI command:
```bash
flask reset-db
```
