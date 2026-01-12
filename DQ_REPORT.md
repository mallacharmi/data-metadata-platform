# Data Quality Report – Sample Dataset

## Dataset

**Name:** sample_dataset  
**Source:** sample.csv  
**Pipeline Job:** pipeline_ingestion

---

## Data Quality Framework

**Tool Used:** Soda Core

---

## Implemented Data Quality Checks

### 1. product_id should not be null

- Rule: column completeness
- Result: PASS

### 2. product_id should be unique

- Rule: uniqueness
- Result: PASS

### 3. price should not be null

- Rule: column completeness
- Result: PASS

### 4. price should be greater than 0

- Rule: numeric constraint
- Result: PASS

### 5. category should not be null

- Rule: column completeness
- Result: PASS

---

## Summary

- Total checks executed: **5**
- Passed: **5**
- Failed: **0**
- Success Percentage: **100%**

---

## Storage

All data quality results are persisted in the metadata catalog and linked to pipeline runs.  
Results can be retrieved using:
GET/datasets/<dataset_id>

---

## Conclusion

The dataset meets all defined data quality expectations and is suitable for downstream usage.
