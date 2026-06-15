# Unified Log Processor Pipelines

Ecossistema de processamento de logs de auditoria e telemetria utilizando Apache Spark, ScyllaDB e AWS S3. O projeto foca em escalabilidade, conformidade com a LGPD e observabilidade avançada para múltiplos domínios de dados.

## Objetivo

Este projeto faz parte da **Unidade V: Projeto Integrador (Capstone)** e implementa um fluxo ETL robusto:

*   **Ingestão:** Consumo de logs brutos do S3 via Boto3/S3A.
*   **Processamento:** Limpeza, anonimização de IPs (Hash SHA-256) e agregação de métricas com PySpark.
*   **Escrita:** Persistência de dados agregados em um cluster ScyllaDB (via conector Cassandra).
*   **Observabilidade:** Monitoramento de execução e logs integrado ao Dynatrace.
*   **Arquivamento:** Movimentação automática de logs processados no S3 para evitar duplicidade.

---

## Arquitetura

```text
       [ AWS S3 ] ----> [ Boto3/S3A ] ----> [ Spark Master ]
                                                  |
                                          [ Spark Workers ] (ETL)
                                                  |
       [ Dynatrace ] <--- [ Logs/Metrics ] <------+------> [ ScyllaDB ]
          (SDK)                                          (Audit Table)

```

---

## Tecnologias Utilizadas

* Python
* Apache Spark 3.5
* ScyllaDB 5.4
* Docker
* Docker Compose
* AWS S3
* PySpark
* Cassandra Connector
* dotenv

---

## Estrutura do Projeto

```text
Unified-Log-Processor-Pipelines
│
├── docker-compose.yml
├── .env
│
├── src
│   ├── scripts
│   │   └── process_logs_ecommerce.py
│   │
│   ├── schemas
│   │   └── schema_logs_ecommerce.py
│   │
│   ├── utils
│   │   ├── initialize_client.py
│   │   └── initialize_spark.py
│   │
│   └── databases
│       └── ecommerce_logs.sql
│
└── README.md
```

---

## Fluxo de Processamento

### 1. Extração

Os arquivos CSV são lidos do bucket S3:

```text
s3://bucket/raw/logs/
```

### 2. Transformação

Durante o processamento são aplicadas regras de negócio:

* Hash SHA-256 para anonimização de IP.
* Remoção de informações sensíveis.
* Tratamento de dados para conformidade com LGPD.
* Agregação de métricas de acesso.

### 3. Carga

Os dados agregados são persistidos em:

```text
Keyspace: ecommerce_logs
Tabela: audit_metrics
```

### 4. Arquivamento

Após o processamento:

```text
raw/logs/
```

é movido para:

```text
archive/logs/
```

evitando reprocessamento.

---

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env`:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

S3_BUCKET_NAME=ecommerce-logs
```

---

## Executando com Docker

### Subir os serviços

```bash
docker compose up -d
```

### Verificar containers

```bash
docker ps
```

### Visualizar logs

```bash
docker compose logs -f
```

---

## Executando o Pipeline

```bash
python src/scripts/process_logs_ecommerce.py
```

---

## Funcionalidades

* Leitura de arquivos CSV em lote.
* Processamento distribuído com Spark.
* Integração com AWS S3.
* Persistência em ScyllaDB.
* Anonimização de dados sensíveis.
* Arquivamento automático.
* Geração de métricas para auditoria.
* Arquitetura preparada para Big Data.

---

## Possíveis Evoluções

* Processamento em Streaming com Spark Structured Streaming.
* Integração com Kafka.
* Dashboard com Grafana.
* Monitoramento com Dynatrace.
* Deploy em Kubernetes.
* Integração com Airflow.
* Particionamento de dados.
* Data Lake Architecture.

---

## Autor

Caio Querino Salustriano Marques

Desenvolvedor Full Stack com foco em Engenharia de Dados, Back-End e Arquiteturas Escaláveis.

LinkedIn:
https://www.linkedin.com/in/caio-querino-1257622a5/

GitHub:
https://github.com/CaioQuerino