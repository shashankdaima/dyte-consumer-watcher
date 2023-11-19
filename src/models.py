from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LogData(Base):
    __tablename__ = 'log_data_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String(255))
    message = Column(Text)
    resource_id = Column(String(255))
    timestamp = Column(TIMESTAMP)
    trace_id = Column(String(255))
    span_id = Column(String(255))
    commit = Column(String(255))
    extra_metadata = Column(JSON)
