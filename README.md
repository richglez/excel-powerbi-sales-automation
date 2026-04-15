# Excel Power BI Sales Automation

## Overview

This project is an end-to-end sales analytics system that integrates Excel (VBA), a Python backend built with Django, and Power BI for data visualization.

It simulates a real-world business workflow where sales data is generated, processed, stored, and visualized through a modern analytics dashboard.

---

## Objective

To design and implement a full data pipeline that automates sales data generation, processing, and visualization.

---

## Tech Stack

* **Excel (VBA):** Data generation and automation
* **Python:** Data processing and backend logic
* **Django (Django REST Framework):** API and backend services
* **Power BI:** Data visualization and dashboarding

---

## Key Features

* Automated sales data generation using Excel macros
* Data export to CSV format
* Backend ingestion and processing of sales data
* REST API for data access
* Interactive dashboards in Power BI
* Data cleaning and transformation
* KPI tracking (revenue, trends, top products)
* Simulation of a real business intelligence workflow

---

## Data Pipeline

```
Excel (VBA)
   ↓
CSV Export
   ↓
Django Backend (API + Processing)
   ↓
Power BI Dashboard
```

---

## Project Structure

```
excel-powerbi-sales-automation/
│
├── excel/
│   └── sales_data.xlsm
│
├── backend/
│   └── django_project/
│
├── powerbi/
│   └── dashboard.pbix
│
├── data/
│   └── sales_data.csv
│
├── images/
│   └── dashboard.png
│
└── README.md
```

---

## Workflow

1. Excel generates synthetic sales data using VBA macros
2. Data is exported to CSV
3. The backend ingests and stores the data
4. API endpoints expose processed data
5. Power BI consumes the data and renders dashboards

---

## API Capabilities (Planned / Implemented)

* Upload CSV data
* Retrieve aggregated sales data
* Filter by product, category, or date
* KPI calculations

---

## Future Improvements

* Automate Excel-to-backend integration via HTTP requests
* Containerize backend using Docker
* Deploy backend to cloud platforms (e.g., Render or Railway)
* Connect Power BI directly to the API instead of static files
* Add authentication and user roles

---

## Use Cases

* Business intelligence dashboards
* Sales performance tracking
* Data pipeline demonstration
* Automation workflows

---

## Notes

This project is designed as a portfolio piece to demonstrate full-stack development combined with data engineering and analytics capabilities.
