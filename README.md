# Hi! Thanks for taking time to review my project. If there are any discrepancies please feel free to contact me using the info below.
Email : amaan5800@gmail.com
Phone : +91 9632309787

# Attention Please 
Ideally I would run the 3 different microservices that I had written using docker containers. 
But because I got the assignment on Saturday afternoon, I had to compromise on few features because of time constraint. 
Thank you for understanding. 

# Video and Guide
I have put the video-guide, demonstration and system design in the link below. Please check it out
https://drive.google.com/drive/folders/1j9SSSBWZZ6cMGaH41L_ZRuPemEH94qf-?usp=drive_link


# Setup

Let us first create a virtual environment and install the packages in requirements.txt

Let us then initialize our Kafka instance. Please make sure you have docker desktop installed

Initialise kafka instance with 'kafka' as working directory 
``` docker
docker-compose -f docker-compose.yml up -d
```
Then create the TimescaleDB instance
``` docker
docker run -d --name timescaledb -p 127.0.0.1:5432:5432 \
-e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg14-latest
```
Now lets us run our three microservices. You have to cd into thier individual directories and run
the below command in separate terminals.
readService , writeService, queryService
``` python
python main.py
```

You can then hit readService at port 3000 with '/ingest' as the api endpoint to populate the logs.
Alternatively you can run 'tests/populator.py' which will hit the endpoint in parallel with sample data.

Finally you can navigate to 'http://127.0.0.1:3003' and then start using the app.

# Features Implemented 
- Web UI for full-text search across logs.
- Filters based on:
    - level
    - message
    - resourceId
    - timestamp
    - traceId
    - spanId
    - commit
    - metadata.parentResourceId
- Efficient and quick search results
- Search within specific date ranges.
- Combining multiple filters.
- Provide real-time log ingestion and searching capabilities.
- Robust scalability using Kafka
- Microservices approach 
- TimescaleDB to create hyper tables and chunks to obtain better time based indexing

# TechStack Used
- Python 
- FastAPI
- Kafka
- Docker 
- PostgresQL
- TimescaleDb
