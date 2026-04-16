import pandas as pd
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Sum, Avg, Count, Max, Min
from django.db.models.functions import TruncDate, TruncMonth

from .models import Sale


# ──────────────────────────────────────────────
# UTILIDAD: parsear query params de fecha
# ──────────────────────────────────────────────


def get_date_filters(request):
    """
    Extrae date_from y date_to de los query params.
    Uso: GET /api/sales/summary/?date_from=2024-01-01&date_to=2024-12-31
    """
    filters = {}
    date_from = request.query_params.get("date_from")
    date_to = request.query_params.get("date_to")

    if date_from:
        try:
            filters["date__gte"] = datetime.strptime(date_from, "%Y-%m-%d").date()
        except ValueError:
            pass

    if date_to:
        try:
            filters["date__lte"] = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError:
            pass

    return filters


# ──────────────────────────────────────────────
# POST /api/sales/upload/
# ──────────────────────────────────────────────


@api_view(["POST"])
def upload_csv(request):
    """
    Recibe un CSV generado desde Excel VBA.
    Inserta registros evitando duplicados exactos.
    """
    file = request.FILES.get("file")

    if not file:
        return Response(
            {"error": "No file provided. Usa key='file' en form-data."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return Response(
            {"error": f"Error leyendo el CSV: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validar columnas esperadas
    required_columns = {"fecha", "producto", "categoria", "precio", "cantidad", "total"}
    if not required_columns.issubset(set(df.columns)):
        return Response(
            {
                "error": f"Columnas requeridas: {required_columns}. Encontradas: {list(df.columns)}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    created_count = 0
    skipped_count = 0
    errors = []

    for index, row in df.iterrows():
        try:
            _, was_created = Sale.objects.get_or_create(
                date=row["fecha"],
                product=row["producto"],
                price=round(float(row["precio"]), 2),
                quantity=int(row["cantidad"]),
                defaults={
                    "category": row["categoria"],
                    "total": round(float(row["total"]), 2),
                },
            )
            if was_created:
                created_count += 1
            else:
                skipped_count += 1

        except Exception as e:
            errors.append({"row": index + 1, "error": str(e)})

    return Response(
        {
            "message": "Upload completado",
            "created": created_count,
            "skipped": skipped_count,
            "errors": errors,
        },
        status=status.HTTP_201_CREATED,
    )


# ──────────────────────────────────────────────
# GET /api/sales/kpis/
# Power BI → Tarjetas KPI principales
# ──────────────────────────────────────────────


@api_view(["GET"])
def sales_kpis(request):
    """
    Retorna métricas globales para las tarjetas KPI del dashboard.
    Soporta filtros: ?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    filters = get_date_filters(request)
    qs = Sale.objects.filter(**filters)

    if not qs.exists():
        return Response({"error": "No hay datos con esos filtros."}, status=404)

    aggregates = qs.aggregate(
        total_revenue=Sum("total"),
        total_quantity=Sum("quantity"),
        total_orders=Count("id"),
        avg_ticket=Avg("total"),
        max_sale=Max("total"),
        min_sale=Min("total"),
    )

    # Top producto
    top_product = (
        qs.values("product").annotate(revenue=Sum("total")).order_by("-revenue").first()
    )

    # Top categoría
    top_category = (
        qs.values("category")
        .annotate(revenue=Sum("total"))
        .order_by("-revenue")
        .first()
    )

    return Response(
        {
            "total_revenue": round(aggregates["total_revenue"] or 0, 2),
            "total_quantity": aggregates["total_quantity"] or 0,
            "total_orders": aggregates["total_orders"] or 0,
            "avg_ticket": round(aggregates["avg_ticket"] or 0, 2),
            "max_sale": round(aggregates["max_sale"] or 0, 2),
            "min_sale": round(aggregates["min_sale"] or 0, 2),
            "top_product": top_product["product"] if top_product else None,
            "top_category": top_category["category"] if top_category else None,
        }
    )


# ──────────────────────────────────────────────
# GET /api/sales/summary/
# Power BI → Tabla: Revenue por producto
# ──────────────────────────────────────────────


@api_view(["GET"])
def sales_summary(request):
    """
    Revenue total y cantidad vendida por producto.
    Soporta filtros: ?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    filters = get_date_filters(request)

    data = (
        Sale.objects.filter(**filters)
        .values("product", "category")
        .annotate(
            total_revenue=Sum("total"),
            total_quantity=Sum("quantity"),
            total_orders=Count("id"),
            avg_price=Avg("price"),
        )
        .order_by("-total_revenue")
    )

    return Response(list(data))


# ──────────────────────────────────────────────
# GET /api/sales/by-category/
# Power BI → Gráfico Donut / Barras por categoría
# ──────────────────────────────────────────────


@api_view(["GET"])
def sales_by_category(request):
    """
    Revenue y cantidad por categoría de producto.
    Soporta filtros: ?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    filters = get_date_filters(request)

    data = (
        Sale.objects.filter(**filters)
        .values("category")
        .annotate(
            total_revenue=Sum("total"),
            total_quantity=Sum("quantity"),
            total_orders=Count("id"),
        )
        .order_by("-total_revenue")
    )

    return Response(list(data))


# ──────────────────────────────────────────────
# GET /api/sales/by-date/
# Power BI → Gráfico de líneas: tendencia diaria
# ──────────────────────────────────────────────


@api_view(["GET"])
def sales_by_date(request):
    """
    Revenue diario para gráfico de tendencia.
    Soporta filtros: ?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    filters = get_date_filters(request)

    data = (
        Sale.objects.filter(**filters)
        .annotate(day=TruncDate("date"))
        .values("day")
        .annotate(
            total_revenue=Sum("total"),
            total_quantity=Sum("quantity"),
            total_orders=Count("id"),
        )
        .order_by("day")
    )

    return Response(list(data))


# ──────────────────────────────────────────────
# GET /api/sales/by-month/
# Power BI → Gráfico de barras: tendencia mensual
# ──────────────────────────────────────────────


@api_view(["GET"])
def sales_by_month(request):
    """
    Revenue mensual agrupado.
    Soporta filtros: ?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    filters = get_date_filters(request)

    data = (
        Sale.objects.filter(**filters)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            total_revenue=Sum("total"),
            total_quantity=Sum("quantity"),
            total_orders=Count("id"),
        )
        .order_by("month")
    )

    return Response(list(data))


# ──────────────────────────────────────────────
# GET /api/sales/top-products/
# Power BI → Gráfico de barras horizontales: Top N productos
# ──────────────────────────────────────────────


@api_view(["GET"])
def top_products(request):
    """
    Top N productos por revenue.
    Soporta: ?limit=10&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    filters = get_date_filters(request)
    limit = int(request.query_params.get("limit", 10))

    data = (
        Sale.objects.filter(**filters)
        .values("product", "category")
        .annotate(
            total_revenue=Sum("total"),
            total_quantity=Sum("quantity"),
            total_orders=Count("id"),
        )
        .order_by("-total_revenue")[:limit]
    )

    return Response(list(data))


# ──────────────────────────────────────────────
# GET /api/sales/raw/
# Power BI → Tabla de datos crudos (opcional)
# ──────────────────────────────────────────────


@api_view(["GET"])
def sales_raw(request):
    """
    Todos los registros crudos para tabla detallada en Power BI.
    Soporta: ?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD&product=Laptop&category=Tecnologia
    """
    filters = get_date_filters(request)

    product = request.query_params.get("product")
    category = request.query_params.get("category")

    if product:
        filters["product__icontains"] = product
    if category:
        filters["category__icontains"] = category

    data = (
        Sale.objects.filter(**filters)
        .values("id", "date", "product", "category", "price", "quantity", "total")
        .order_by("-date")
    )

    return Response(list(data))
