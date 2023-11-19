from models import LogData
from utils.get_sql_engine_and_session import get_engine_and_session
import json
from datetime import datetime
import os
from models import LogData
from dotenv import load_dotenv
import redis

load_dotenv()

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
            self.close_session()
        except Exception as e:
            self.session.rollback()
            print(f"Error inserting profile row: {str(e)}")
            self.close_session()

def send_log_to_supabase(uid):
    engine, Session=get_engine_and_session()
    worker=PostgreSQL_Worker(engine, Session)

    redis_host=os.environ.get("REDIS_PUBLIC_ENDPOINT_HOST")
    redis_port=int(os.environ.get("REDIS_PUBLIC_ENDPOINT_PORT"))
    redis_password=os.environ.get("REDIS_PASSWORD")

    redis_instance = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
    )

    json_data=json.loads(redis_instance.get(uid))
    # Convert timestamp string to a datetime object
    timestamp = datetime.strptime(json_data["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
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
    redis_instance.delete(uid)