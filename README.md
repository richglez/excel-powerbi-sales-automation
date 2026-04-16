# Excel Power BI Sales Automation

## Overview

**Excel Power BI Sales Automation** is an end-to-end data pipeline that simulates a real-world sales analytics workflow.

The system integrates **Excel (VBA)** for data generation, a **Django-based backend** for ingestion and processing, and **Power BI** for visualization. It demonstrates how raw transactional data can be transformed into actionable business insights through a modern analytics stack.

This project is designed to showcase **full-stack development, data engineering, and business intelligence capabilities.**

---

## Tech Stack

| **Technology**  | **Layer**          |
| --------------- | ------------------ |
| Excel VBA       | Data Generation    |
| Python / Django | Backend            |
| Pandas          | Data Processing    |
| Power BI        | Visualization      |
| REST            | API Communication  |



---

## Features

### Data Generation
* Automated synthetic sales data generation (200+ records per run)
* Configurable randomness (products, categories, dates, revenue)

### Data Ingestion
* CSV-based ingestion pipeline
* Planned: Direct Excel → API integration via HTTP (VBA POST requests)

### Backend Processing
* Data cleaning and normalization using Pandas
* Aggregation logic for KPIs and analytics
* Scalable service layer using Django architecture

### API Layer
* RESTful endpoints for:
  * Data ingestion
  * Aggregated sales metrics
  * Filtering (date, product, category)
* Designed for BI tool consumption

### Data Visualization
* Interactive dashboards in Power BI
* KPI tracking:
  * Revenue trends
  * Top-performing products
  * Sales distribution

---


## Project Structure

```
excel-powerbi-sales-automation/
├── backend/              # Django project
├── sales/                # Core app (models, views, logic)
├── excel/                # VBA-enabled Excel file
├── data/                 # Generated CSV files
├── powerbi/              # Power BI dashboard (.pbix)
├── images/               # Dashboard previews
├── venv/                 # Virtual environment
└── README.md
```

---

## Workflow

1. Excel generates synthetic sales data using VBA
2. Data is exported to CSV or sent via HTTP request
3. Django backend ingests and processes the data
4. Aggregations and KPIs are calculated
5. Power BI consumes the processed data
6. Dashboards visualize business insights

---



---

## Use Cases

* Business intelligence dashboards
* Sales performance tracking
* Data pipeline demonstration
* Automation workflows

---


## Installation
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install django djangorestframework pandas

# Setup project
django-admin startproject backend
cd backend
python manage.py startapp sales

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver
```


## Documentation
[PRD](docs/planning/PRD.md) - Product Requirements Document
[Roadmap](docs/planning/roadmap.md) - Schema de base de datos
[Architecture](docs/architecture/architecture.md) - Architecura
[Models](docs/architecture/scheme.md) - Diagrams
[API](docs/api/docs_APIRoutes.txt) - API Routes

## Licence
MIT
