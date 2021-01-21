import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import _app_ctx_stack

class SQLAlchemy_bind:
    def __init__(self, app=None):
        """Initialize aspects of self to None as it should
         be called initialized outside of app context."""
        self.app = app
        if app:
            self.init_app(app)

    def init_session_maker(self):
        """The session maker is initialized at one point
        in the program and then called later to return 
        Session() objects from the registry. 
        
        In the next update: Ability to instantiate it 
        in the init portion of your codebase and bind the 
        engine using sessionmaker.configure()"""
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine)

    def init_scoped_session(self):
        """Creates a single scoped_session registry 
        when the web application first starts, ensuring that 
        this object is accessible by the rest of the 
        application."""
        return scoped_session(self.sessionmaker, scopefunc=_app_ctx_stack.__ident_func__)

    def init_db(self):
        """Creates all tables in connected database (or
        just the new ones) according to specific app's
        specifications."""
        self.Base.metadata.create_all(bind=self.engine)

    def empty_db(self):
        """Drops all tables in connected database."""
        self.Base.metadata.drop_all(bind=self.engine)
    
    def end_session(self, error=None):
        """Removes the current Session object associated with
        the request/thread. It should catch and report errors."""
        self.session.remove()
        # can I handle a db integrity error here and do a rollback??
        if error:
            # Log the error
            print("logging error", str(error))

    def init_app(self, app=None):
        """Set up SQLAlchemy to be used with a specific app.
        Connect the database and create a scoped_session object
        to manage the local Session instances. Add teardown_request
        decorator to app to instruct the scoped_session registery
        to remove the Session after each request."""
        if app:
            self.app = app
            try:
                self.Base = declarative_base()
                # connect database
                self.engine = sqlalchemy.create_engine(self.app.config['DATABASE'])
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
                print("Error connecting database.\nPlease set app.config['DATABASE'] to your database connection string")
        else:
            print("SQLAlchemy could not be set up.\nUsage:\nOutside app factory\n>> db = SQLAlchemy()\nInside app factory\n>> db.init_app(your_flask_app)")
