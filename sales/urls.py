from django.urls import path
from .views import (
    upload_csv,
    sales_kpis,
    sales_summary,
    sales_by_category,
    sales_by_date,
    sales_by_month,
    top_products,
    sales_raw,
)

urlpatterns = [
    # Ingesta
    path("upload/", upload_csv, name="upload-csv"),
    # Power BI endpoints
    path("kpis/", sales_kpis, name="sales-kpis"),
    path("summary/", sales_summary, name="sales-summary"),
    path("by-category/", sales_by_category, name="sales-by-category"),
    path("by-date/", sales_by_date, name="sales-by-date"),
    path("by-month/", sales_by_month, name="sales-by-month"),
    path("top-products/", top_products, name="top-products"),
    path("raw/", sales_raw, name="sales-raw"),
]
