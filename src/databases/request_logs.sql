CREATE KEYSPACE IF NOT EXISTS request_logs
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE request_logs.audit_metrics (
    uri text PRIMARY KEY,
    total_accesses bigint,
    unique_visitors bigint,
    avg_response_size double,
    success_count bigint,
    error_count bigint,
    processed_at timestamp
);