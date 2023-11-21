## Up container detached state
docker-compose -p log_ingestor -f docker-compose.yml up -d

## Run test producer
docker run -it --rm --network kafka_docker confluentinc/cp-kafka /bin/kafka-console-producer --bootstrap-server kafka:9092 --topic logstream

## Run test consuemr
docker run -it --rm --network kafka_docker confluentinc/cp-kafka /bin/kafka-console-consumer --bootstrap-server kafka:9092 --topic logstream

## Exec into the container
## Git bash(Windows)
winpty docker exec -it <container_id> //bin//sh 
## Linux
docker exec -it <container-id> /bin/sh

## Create topic 
./opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic logstream

## List Topics
./opt/kafka/bin/kafka-topics.sh --list --zookeeper zookeeper:2181

## Write events
docker exec -ti kafka-kafka-1 ./opt/kafka/bin/kafka-console-producer.sh --topic logstream --bootstrap-server localhost:9092
Exit the producer using Ctrl + D

## Read events
./opt/kafka/bin/kafka-console-consumer.sh --topic logstream --from-beginning --bootstrap-server localhost:9092

## Create Timescale instance
### Query Interface:
docker run -d --name timescaledb -p 127.0.0.1:5432:5432 \
-e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg14-latest

## Connect to DB
docker exec -it timescaledb psql -U postgres

## Get address of docker container 
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' your_container_name_or_id

## Connection URL DB
DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"