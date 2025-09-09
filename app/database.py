from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from . import config

sqlalchemy_database_url = f"postgresql://{config.settings.database_username}:{config.settings.database_password}@{config.settings.database_hostname}:{config.settings.database_port}/{config.settings.database_name}"
engine = create_engine(sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="Fastapi",
#             user="postgres",
#             password="toor",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("---------------------------------------")
#         print("Database connection was successful!")
#         print("---------------------------------------")
#         cursor.execute("SELECT * FROM posts")
#         my_posts = cursor.fetchall()
#         break
#     except Exception as error:
#         print("---------------------------------------")
#         print("connecting to the database failed!")
#         print("error:", error)
#         print("---------------------------------------")
#         time.sleep(3)
