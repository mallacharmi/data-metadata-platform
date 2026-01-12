# Data Metadata Platform 🚀

## Build a Data Metadata Platform with Flask, PostgreSQL, and OpenLineage

**Author:** Malla Charmi  
**Domain:** Data Engineering  
**Difficulty:** Hard  

---

## 📌 Project Overview

This project implements a **mini Data Metadata Platform** demonstrating core data governance concepts:

- Metadata Catalog
- Data Quality Monitoring
- Data Lineage Tracking

The system is built using **Flask**, **PostgreSQL**, **Docker**, **Python**, **Soda Core**, and **OpenLineage-style events**.

---

## 🏗️ System Architecture

### Services

- **metadata-api** – Flask REST API for metadata
- **metadata-postgres** – PostgreSQL metadata store
- **pipeline** – Python ingestion & DQ pipeline

All services are orchestrated with **Docker Compose**.

---

## 🧱 Metadata Entities

- Dataset
- Schema (columns)
- Data Quality Results
- Lineage Edges

---

## 🌐 API Endpoints

### Health
GET /health/lineage

### Datasets
POST /datasets  
GET /datasets/<id>  
POST /datasets/<id>/schema  

### Search
GET /search?q=<keyword>

### Data Quality
POST /dq-results

### Lineage
GET /datasets/<id>/lineage  
POST /openlineage/events

---

## 🔄 Pipeline Flow

1. Waits for API readiness
2. Reads CSV data
3. Registers dataset
4. Extracts schema & stats
5. Runs Soda Core checks
6. Stores DQ results
7. Emits lineage
8. Pipeline completes

---

## ▶️ How to Run

```bash
docker-compose up --build -d
docker-compose run pipeline
```

---

## ✅ Validation

```bash
curl http://localhost:5000/health/lineage
curl "http://localhost:5000/search?q=sample"
curl http://localhost:5000/datasets/1
curl http://localhost:5000/datasets/1/lineage
```

---

## 📦 Project Structure

```
data-metadata-platform/
├── api/
├── pipeline/
├── data/
├── examples/
├── dq_report.md
├── submission.yml
├── docker-compose.yml
└── README.md
```

---

## 🏁 Status

✅ Fully implemented and ready for submission
