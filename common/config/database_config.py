from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv()

conn_url = URL.create(
    drivername= os.getenv("DRIVERNAME"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    port=os.getenv("PORT")
)
db_engine = create_engine(conn_url)
session = sessionmaker(autoflush=False, bind = db_engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()