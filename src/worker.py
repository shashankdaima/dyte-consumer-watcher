from models import LogData
from utils.get_sql_engine_and_session import get_engine_and_session
import json
from datetime import datetime

class PostgreSQL_Worker():
    def __init__(self,engine, Session):
        self.session = Session()

    def close_session(self):
        if self.session.is_active:
            self.session.close()

    def pushRecord(self,record):
        try:
            self.session.add(record)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error inserting profile row: {str(e)}")

engine, Session=get_engine_and_session()
worker=PostgreSQL_Worker(engine, Session)
json_data = {
    "level": "error",
    "message": "Failed to connect to DB",
    "resourceId": "server-1234",
    "timestamp": "2023-09-15T08:00:00Z",
    "traceId": "abc-xyz-123",
    "spanId": "span-456",
    "commit": "5e5342f",
    "metadata": {
        "parentResourceId": "server-0987"
    }
}

# Convert timestamp string to a datetime object
timestamp = datetime.strptime(json_data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")

# Create an instance of LogData
log_entry = LogData(
    level=json_data["level"],
    message=json_data["message"],
    resource_id=json_data["resourceId"],
    timestamp=timestamp,
    trace_id=json_data["traceId"],
    span_id=json_data["spanId"],
    commit=json_data["commit"],
    extra_metadata=json.dumps(json_data["metadata"])
)
worker.pushRecord(log_entry)