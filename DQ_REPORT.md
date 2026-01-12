# Data Quality Report – Sample Dataset

## Dataset Details

- **Dataset Name:** sample_dataset
- **Source File:** sample.csv
- **Pipeline Job:** pipeline_ingestion

---

## Data Quality Framework

- **Tool Used:** Soda Core

---

## Defined Data Quality Checks

The following data quality rules are defined and executed as part of the data ingestion pipeline:

### 1. product_id should not be null

- Rule Type: Column completeness

### 2. product_id should be unique

- Rule Type: Uniqueness constraint

### 3. price should not be null

- Rule Type: Column completeness

### 4. price should be greater than zero

- Rule Type: Numeric constraint

### 5. category should not be null

- Rule Type: Column completeness

---

## Example Execution Summary

| Metric               | Value |
| -------------------- | ----- |
| Total checks defined | 5     |
| Checks executed      | 5     |
| Passed checks        | 5     |
| Failed checks        | 0     |
| Success percentage   | 100%  |

> **Note:**  
> This summary represents a successful validation scenario.  
> Actual pipeline executions may produce PASS or FAIL results depending on input data quality.  
> All execution results are persisted in the metadata catalog.

---

## Storage & Retrieval

All data quality results are:

- Stored in PostgreSQL via the Metadata API
- Linked to the dataset and pipeline run
- Queryable through the API

### Verification Endpoint

```bash
GET /datasets/<dataset_id>
```

Example:
curl http://localhost:5000/datasets/1



### Conclusion

This project successfully integrates a data quality framework into the metadata platform.
It demonstrates the ability to define, execute, persist, and expose data quality results, fulfilling modern data governance requirements.
