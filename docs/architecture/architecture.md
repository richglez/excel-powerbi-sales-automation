# Architecture

## Data Pipeline
The system follows a modular data pipeline architecture:

```
Excel (VBA)
   ↓
CSV Export
   ↓
HTTP Request
   ↓
Django REST API (Data Ingestion & Processing)
   ↓
Power BI Dashboard
```


