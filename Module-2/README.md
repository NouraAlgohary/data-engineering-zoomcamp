# Workflow Orchestration

- Introduction

## Introduction
In the first module, we demonstrated the creation of an automated data pipeline using Docker, Python, and PostgreSQL. The pipeline downloaded data from the web, transforms it, and loads it into a PostgreSQL database for analysis. The project also includes a Dockerized environment with pgAdmin for database management.

**Problems**
- No Error Recovery: If the database step fails, the whole script restarts, including re-downloading the data.
- No Retry Logic: Adding retries for each step (download, transform, insert) is complicated and messy.
- Not Generalizable: The pipeline is built for specific data sources (e.g., taxi data and zone data). Adding new data sources requires rewriting parts of the script, which is time-consuming and error-prone.
- No Checkpoints: If one step fails, the pipeline can’t resume from where it left off. It starts over.
- Manual Runs: The pipeline must be started manually, which isn’t practical for regular use.

**Ways to solve these problems**

- Modular Design: Break the pipeline into smaller, reusable components (e.g., download, transform, load).
- Configuration Files:
Use config files (e.g., JSON or YAML) to define data sources, transformations, and database settings.
- Parameterization:
Allow the script to accept parameters (e.g., file paths, table names) to handle different data sources dynamically.
- Workflow Orchestration:
Tools like Apache Airflow or Prefect can help manage and generalize complex workflows.

**Improvements Made**

- Configuration Files:
  - Added YAML/JSON config files to define data sources, transformations, and database settings.
  - This makes it easier to modify the pipeline (e.g., adding new data sources) without changing the code.
- Parameterization:
  - Updated the script to accept dynamic parameters (e.g., file paths, table names) for handling different data sources.
  - This makes the pipeline more flexible and reusable for various use cases.

------------
## Conceptual Material: Introduction to Orchestration and Kestra
------------
## Hands-On Coding Project: Build Data Pipelines with Kestra
In this project, we are going to build a **ETL Pipeline** using **Kestra**. 
Project Steps:
1. Extract data from NYC’s Taxi and Limousine Commission (TLC) CSV files.
2. Load the data into **PostgreSQL** or **Google Cloud** (**GCS**+ **BigQuery**)
3. Explore scheduling and backfilling workflows.

Prerequisites:
- **Docker** and **Docker Compose** installed on your machine.
- Basic understanding of **ETL**, **PostgreSQL**, and **Kestra**.

Steps:
1. Clone the project
Clone the repo
```
git clone https://github.com/DataTalksClub/data-engineering-zoomcamp.git
```
Change Directory to ```02-workflow-orchestration```
```
cd 02-workflow-orchestration/
```
2. Set Up Kestra with Docker Compose
Start the Docker containers for Kestra and PostgreSQL:
```
docker compose up -d
```
This will:
- Start a Kestra server container.
- Start a PostgreSQL containers.

<img width="591" alt="Screenshot 2025-02-02 at 11 24 53 AM" src="https://github.com/user-attachments/assets/887ede49-0c8f-4da4-88fe-5f372e51ec0e" />

Access the Kestra UI at __http://localhost:8080__.

3. Set Up Kestra with Docker Compose

To import flows, run the following commands on bash:
```
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/01_getting_started_data_pipeline.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/02_postgres_taxi.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/02_postgres_taxi_scheduled.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/03_postgres_dbt.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/04_gcp_kv.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/05_gcp_setup.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/06_gcp_taxi.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/06_gcp_taxi_scheduled.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/07_gcp_dbt.yaml
```



<img width="1377" alt="Screenshot 2025-02-02 at 11 34 09 AM" src="https://github.com/user-attachments/assets/34c93a69-7d4e-4525-b254-39142f44a5b2" />


