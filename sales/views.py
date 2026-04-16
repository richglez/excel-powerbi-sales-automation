import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sale
from django.db.models import Sum


@api_view(["POST"])
def upload_csv(request):
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file provided"}, status=400)

    df = pd.read_csv(file)

    for _, row in df.iterrows():
        Sale.objects.create(
            date=row["fecha"],
            product=row["producto"],
            category=row["categoria"],
            price=row["precio"],
            quantity=row["cantidad"],
            total=row["total"],
        )

    return Response({"message": "Data uploaded successfully"})

# Endpoint para análisis (Power BI)
@api_view(["GET"])
def sales_summary(request):
    data = (
        Sale.objects.values("product")
        .annotate(total_sales=Sum("total"))
        .order_by("-total_sales")
    )

    return Response(data)
