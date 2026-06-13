-- Configuração inicial para o ScyllaDB (Compatível com Cassandra)

-- 1. Criação do Keyspace para isolamento dos dados de e-commerce
CREATE KEYSPACE IF NOT EXISTS ecommerce_logs 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- 2. Criação da tabela de métricas de auditoria conforme o processamento PySpark
CREATE TABLE IF NOT EXISTS ecommerce_logs.audit_metrics (
    membership text PRIMARY KEY,
    total_accesses bigint,
    processed_at timestamp
);