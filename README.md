# Flask SQLAlchemy Bind

Minimalistic extension to add support for the SQLAlchemy ORM to your Flask app. Adds most essential functionality - the database table construction is still be figured out. If you're interested in my reasoning behind how I built this and how it all works, [read more here](https://kellylynnfoulk.medium.com/under-the-hood-of-flask-sqlalchemy-793f7b3f11c3). 

## Set Up:
Install using pip:
```bash
pip install flask-sqlalchemy-bind
```

## Setting up Your Flask App

Here's [an example](https://github.com/klfoulk16/demo-flask-sqlalchemy-bind) of a full-fledged (but small) Flask app that uses Flask-SQLAlchemy-Bind. Please poke around.

### Using an App Factory

I recommend using Flask-SQLAlchemy-Bind with an app factory like so:

```python
    from flask import Flask
    from flask_sqlalchemy_bind import SQLAlchemy_bind

    # outside of app factory
    db = SQLAlchemy_bind()

    # must be defined after db = SQLAlchemy_bind() if in same module
    from sqlalchemy import Column, Integer, String
    class User(db.Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)
        password = Column(String, unique=True)

        def __init__(self, username=None, password=None):
            self.username = username
            self.password = password

    # app factory
    def create_app():
        app = Flask(__name__)
        app.config["DATABASE"] = "sqlite:///:memory:"
        # import your database tables if defined in a different module
        # for example if the User model above was in a different module:
        from your_application.database import User
        db.init_app(app)
        return app
```

### Without an App Factory

The following is an example of a Flask app that does not use the app factory pattern:

```python
    from flask import Flask
    from flask_sqlalchemy_bind import SQLAlchemy_bind

    app = Flask(__name__)
    app.config["DATABASE"] = "sqlite:///:memory:"
    db = SQLAlchemy_bind()

    # define your database tables
    from sqlalchemy import Column, Integer, String
    class User(db.Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)
        password = Column(String, unique=True)

        def __init__(self, username=None, password=None):
            self.username = username
            self.password = password

    # set up SQLAlchemy for your app
    # you must import or define your database tables before running this
    db.init_app(app)

    db.session.add(User(username="Hi", email="itsme@example.com"))
    db.session.commit()

    users = User.query.all()
```

## Adding a CLI Command to Reset the Database

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
