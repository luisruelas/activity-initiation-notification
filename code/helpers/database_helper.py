import os
from typing import List
from sqlalchemy import func,cast, Date, create_engine, Column, Integer, String, DateTime, ForeignKey, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import sqlalchemy
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

class Credential(Base):
    __tablename__ = 'credentials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    brand_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

class ApplicationIdentifier(Base):
    __tablename__ = 'application_identifiers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    risk_score_version = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    push_id = Column(String, nullable=False)
    auth_id = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)
    language = Column(String, nullable=False)
    timezone_offset = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
    


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

    def get_possible_application_identifiers(self) -> List[sqlalchemy.engine.row.Row]:
        session = self.get_session()
        try:
            TIME_TO_DELIVER = 19
            MIN_DAY_LAST_ACTIVE = 4
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            now_current_timezone = datetime.datetime.now()
            UTC_HOUR_NOW = 24 if now_utc.hour == 0 else now_utc.hour
            raw_offset_to_send = TIME_TO_DELIVER - UTC_HOUR_NOW
            offset_to_send = ((raw_offset_to_send + 12) % 24) - 12
            two_days_ago = now_current_timezone - datetime.timedelta(days=2)
            stats_of_two_days_ago = datetime.datetime.combine(two_days_ago, datetime.time.min)
            stats_of_two_days_ago = stats_of_two_days_ago + datetime.timedelta(hours=(offset_to_send * -1))
            min_day_last_active = now_current_timezone - datetime.timedelta(days=MIN_DAY_LAST_ACTIVE)
            stats_min_last_day_active = datetime.datetime.combine(min_day_last_active, datetime.time.min)
            stats_min_last_day_active = stats_min_last_day_active + datetime.timedelta(hours=(offset_to_send * -1))

            application_identifiers = session.query(
                ApplicationIdentifier,
                func.coalesce(Credential.brand_id, 0).label("brand_id")
            ).outerjoin(
                Credential, ApplicationIdentifier.user_id == Credential.user_id
            ).filter(
                ApplicationIdentifier.created_at < stats_of_two_days_ago,
                # ApplicationIdentifier.updated_at >= stats_min_last_day_active,
                func.coalesce(ApplicationIdentifier.timezone_offset, -6) == offset_to_send

            )
            print("DatabaseHelper#get_application_identifiers_created_yesterday", application_identifiers.statement.compile(compile_kwargs={"literal_binds": True}))
            application_identifiers = application_identifiers.all()

            return application_identifiers
        finally:
            session.close()

