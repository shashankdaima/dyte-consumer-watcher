import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
def get_engine_and_session():
    load_dotenv()
    
    db_config = {
        "user": os.environ.get("SQL_USERNAME"),
        "password": os.environ.get("SQL_PASSWORD"),
        "host": os.environ.get("SQL_HOST"),
        "port": int(os.environ.get("SQL_PORT")),  
        "database": os.environ.get("SQL_DB_NAME"),
    }
    print(db_config)
    DB_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    print(DB_URL)
    # Create a SQLAlchemy engine
    engine = create_engine(DB_URL)

    # Create a session
    Session = sessionmaker(bind=engine)
    return engine, Session
