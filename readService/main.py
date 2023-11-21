import asyncio
import json

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, HTTPException
from models import ProducerResponse, LogIngestModel

app = FastAPI()

loop = asyncio.get_event_loop()
KAFKA_INSTANCE = "localhost:9092"
aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_INSTANCE)

@app.post("/ingest")
async def kafka_produce(msg: LogIngestModel):
    try:
        topicname = "logstream"
        await aioproducer.send(topicname, json.dumps(msg.model_dump()).encode("ascii"))
        return "log ingested"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))

@app.on_event("startup")
async def startup_event():
    await aioproducer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()
    await asyncio.sleep(7)

#Terminal Coloring
import colorama
import uvicorn
colorama.init()

if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, log_level="info")