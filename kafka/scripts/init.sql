-- Create normal PostgreSQL table
CREATE TABLE logs (
    id SERIAL ,
    level TEXT,
    message TEXT,
    resourceId TEXT,
    timestamp TIMESTAMPTZ NOT NULL,
    traceId TEXT,
    spanId TEXT,
    commit TEXT,
    parentResourceId TEXT NOT NULL
);

-- Create a hypertable for time-series data based on the timestamp column
SELECT create_hypertable('logs', 'timestamp', if_not_exists => TRUE);

-- Create additional Index
CREATE INDEX IF NOT EXISTS idx_level ON logs (level);
