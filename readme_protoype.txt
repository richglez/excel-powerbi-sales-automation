1. generador de ventas código generador automático de datos de prueba. Lo que hace es "inventar" 200 filas de ventas aleatorias y escribirlas en tu hoja de Excel de un tirón.



2. Features:
* Exportar a CSV (clave para backend)
* Built REST API using Django
* Implemented CSV ingestion pipeline
* Data aggregation and analytics endpoints
* Integrated backend with Excel-generated data

3. Installation
```bash
python -m venv venv
venv\Scripts\activate   # Windows

pip install django djangorestframework pandas
django-admin startproject backend
cd backend
python manage.py startapp sales
python manage.py makemigrations
python manage.py migrate    # Crear migracion
python manage.py runserver  # Ejecutar servidor
```

4. Stack Flow
1️⃣ Conectar Excel → Django automáticamente (🔥)
VBA hace POST al endpoint
2️⃣ Conectar Power BI → API
Power BI consume summary/

