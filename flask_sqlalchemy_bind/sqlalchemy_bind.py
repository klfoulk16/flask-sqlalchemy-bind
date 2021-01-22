import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import _app_ctx_stack

class SQLAlchemy_bind:
    def __init__(self):
        """Create instance of SQLAlchemy connector with the declarative extension"""
        self.Base = declarative_base()

    def init_session_maker(self):
        """Create SQLAlchemy sessionmaker object with desired configuration"""
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine)

    def init_scoped_session(self):
        """Creates a SQLAlchemy scoped_session object"""
        return scoped_session(self.sessionmaker, scopefunc=_app_ctx_stack.__ident_func__)

    def init_db(self):
        """Creates tables in connected database according to defined models."""
        self.Base.metadata.create_all(bind=self.engine)

    def empty_db(self):
        """Drops all tables in connected database."""
        self.Base.metadata.drop_all(bind=self.engine)
    
    def end_session(self, error=None):
        """Removes the current Session object associated with
        the request."""
        self.session.remove()
        if error:
            print("logging error: ", str(error))

    def init_app(self, app=None):
        """Set up SQLAlchemy to be used with a specific app."""
        if app:
            try:
                # connect database
                self.engine = sqlalchemy.create_engine(app.config['DATABASE'])
                # create session factory
                self.sessionmaker = self.init_session_maker()
                # access scoped session registery (implicitely)
                self.session = self.init_scoped_session()
                # add ability to query against the tables
                self.Base.query = self.session.query_property()
                # make sure db is initialize and up to date
                self.init_db()
                # call scoped_session.remove() after each request to scope
                # the session objects to each request
                app.teardown_request(self.end_session)
            except Exception:
                print("Error connecting database.")
                print("Please set app.config['DATABASE'] to your database connection string")
        else:
            print("SQLAlchemy was not set up properly."
            print("Usage:")
            print("Outside app factory")
            print(">> db = SQLAlchemy()")
            print("Inside app factory")
            print(">> db.init_app(your_flask_app)")
