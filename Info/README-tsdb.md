{
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

## Create nomral postgresQL table
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(255),
    message TEXT,
    resourceId VARCHAR(255),
    timestamp TIMESTAMPTZ,
    traceId VARCHAR(255),
    spanId VARCHAR(255),
    commit VARCHAR(255),
    parentResourceId VARCHAR(255) 
);

## Create a hypertable for time-series data based on the timestamp column
SELECT create_hypertable('logs', 'timestamp');

## Create additional Index
CREATE INDEX idx_level ON logs (level);

## Check for indexes
SELECT
    indexname AS index_name,
    indexdef AS index_definition
FROM
    pg_indexes
WHERE
    tablename = 'logs';

## Connect to DB and run script
docker exec -it timescaledb psql -U postgres 

\i /path/to/script.sql

## If inside the container
psql -U postgres -d postgres -a -f /path/to/script.sql