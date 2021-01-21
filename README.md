# Flask SQLAlchemy Bind

Minimalistic extension to add support for the SQLAlchemy ORM to your Flask app. Adds most essential functionality - the database table construction is still be figured out.

## Set Up:
Install using pip:
```bash
pip install flask-sqlalchemy-bind
```

## Setting up You Flask App
A simple Flask app setup using Flask-SQLAlchemy-Bind:
```python
    from flask import Flask
    from flask_sqlalchemy_bind import SQLAlchemy_bind

    app = Flask(__name__)
    app.config["DATABASE"] = "sqlite:///:memory:"
    db = SQLAlchemy_bind(app)

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

### Using an App Factory
You can also use Flask-SQLAlchemy bind with an app factory.

```python
    from flask import Flask
    from flask_sqlalchemy_bind import SQLAlchemy_bind

    # outside of app factory
    db = SQLAlchemy_bind(app)

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
        db.init_app(app)
        return app
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
