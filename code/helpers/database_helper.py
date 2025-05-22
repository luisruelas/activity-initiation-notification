import os
from typing import List
from sqlalchemy import func,cast, Date, create_engine, Column, Integer, String, DateTime, ForeignKey, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

# Load environment variables from .env file

# Database connection details from the .env file
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")

# Base declarative class for SQLAlchemy models
Base = declarative_base()

class ApplicationIdentifier(Base):
    __tablename__ = 'application_identifiers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    risk_score_version = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    push_id = Column(String, nullable=False)
    auth_id = Column(String, nullable=False)
    language = Column(String, nullable=False)
    timezone_offset = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

ENGINE = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# Database Helper Class
class DatabaseHelper:
    def __init__(self):
        self.Session = sessionmaker(bind=ENGINE)

    def get_session(self):
        """
        Create and return a new session for the database connection.
        """
        return self.Session()

    def get_application_identifiers_created_yesterday(self) -> List[ApplicationIdentifier]:
        session = self.get_session()
        try:
            TIME_TO_DELIVER = 17
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            now_current_timezone = datetime.datetime.now()
            UTC_HOUR_NOW = now_utc.hour
            offset_to_send = TIME_TO_DELIVER - UTC_HOUR_NOW
            yesterday = now_current_timezone - datetime.timedelta(days=1)
            start_of_yesterday = datetime.datetime.combine(yesterday, datetime.time.min)
            start_of_yesterday = start_of_yesterday + datetime.timedelta(hours=(offset_to_send * -1))
            end_of_yesterday = datetime.datetime.combine(yesterday, datetime.time.max)
            end_of_yesterday = end_of_yesterday + datetime.timedelta(hours=(offset_to_send * -1))

            application_identifiers = session.query(ApplicationIdentifier).filter(
                ApplicationIdentifier.created_at >= start_of_yesterday,
                ApplicationIdentifier.created_at <= end_of_yesterday,
                func.coalesce(ApplicationIdentifier.timezone_offset, -6) == offset_to_send
            )
            print("DatabaseHelper#get_application_identifiers_created_yesterday", application_identifiers.statement.compile(compile_kwargs={"literal_binds": True}))
            application_identifiers = application_identifiers.all()

            return application_identifiers
        finally:
            session.close()

