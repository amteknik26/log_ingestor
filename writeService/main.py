import asyncio
import json
from pydantic import BaseModel, StrictStr
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, DateTime, JSON, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
Base = declarative_base()

loop = asyncio.get_event_loop()
KAFKA_INSTANCE = "localhost:9092"
consumer = AIOKafkaConsumer("logstream", bootstrap_servers=KAFKA_INSTANCE, loop=loop)

DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
            log_data = msg.value.decode("utf-8")
            await write_log_to_database(log_data)
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
    except Exception as e:
        print(f"Db level exception occured {str(e)}")
        return 
    
    finally:
        await consumer.stop()

async def write_log_to_database(log_data):
    try:
        log_entry = json.loads(log_data)
        insert_log_into_database(log_entry)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def insert_log_into_database(log_entry):
    try:
        with SessionLocal() as db:
            insert_query = text(
            """
            INSERT INTO logs (level, message, resourceId, timestamp, traceId, spanId, commit, parentResourceId)
            VALUES (:level, :message, :resourceId, :timestamp, :traceId, :spanId, :commit, :parentResourceId)
            """
            )
            parent_resource_id = log_entry.get('metadata', {}).get('parentResourceId', None)
            log_entry['parentResourceId'] = parent_resource_id
            result = db.execute(insert_query, log_entry)
            db.commit()
            if result.rowcount > 0:
                print("Record successfully written to the database.")
            else:
                print("No records were inserted.")
    except Exception as e:
        print(f"Exception occured as: {e}")



@app.on_event("startup")
async def startup_event():
    loop.create_task(consume())

@app.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()
    await asyncio.sleep(7)  

#Terminal Coloring
import colorama
import uvicorn
colorama.init()

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", port=3001, log_level="info")
    finally:
        loop.run_until_complete(consumer.stop())
        loop.close()

