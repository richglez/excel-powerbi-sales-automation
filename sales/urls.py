from django.urls import path
from .views import upload_csv, sales_summary

urlpatterns = [
    path("upload/", upload_csv),
    path("summary/", sales_summary),
]
