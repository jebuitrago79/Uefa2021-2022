# ⚽ UEFA Players API - Proyecto FastAPI

Este proyecto está construido con **FastAPI** y permite comparar las métricas de jugadores del videojuego **FIFA 22** con el rendimiento real de jugadores en la **UEFA Champions League 2021-2022**.

---

## 🚀 Características principales

- Gestión de **jugadores FIFA** y **estadísticas UEFA** como modelos independientes.
- CRUD completo para ambos modelos (`GET`, `POST`, `PUT`, `DELETE`).
- Exportación de datos a archivos `.csv`.
- Filtros dinámicos:
  - Filtrar jugadores por país.
  - Filtrar players por valor de `overall`.
- Eliminación lógica en el modelo `Player` (trazabilidad con `is_active`).
- Separación del código por responsabilidades (`crud_*.py`, `main.py`, `models_sqlmodel.py`, etc.).
- Integración de análisis estadístico (regresión y correlaciones) con `statsmodels`.
- Base de datos en **PostgreSQL alojada en Clever Cloud**.
- Backend desplegado en **Render.com**.

---

## 🧭 Mapa de Endpoints

### 🔹 Generales
- `GET /` → Mensaje de bienvenida
- `GET /hello/{name}` → Saludo personalizado

### 🔹 Jugadores FIFA
- `GET /jugadores`
- `GET /jugadores/{id}`
- `POST /jugadores`
- `PUT /jugadores/{id}`
- `DELETE /jugadores/{id}`
- `GET /jugadores/filtrar/pais/{pais}`
- `GET /jugadores1/export`

### 🔹 Estadísticas UEFA
- `GET /players`
- `GET /players/{id}`
- `POST /players`
- `PUT /players/{id}`
- `DELETE /players/{id}` → (eliminación lógica)
- `GET /players/filter/overall?min_overall=`
- `GET /players1/export`
- `GET /players1/eliminados`

---

🌐 URLs del despliegue
Render: https://uefa2021-2022.onrender.com


Autor
Julian Buitrago Camacho
Proyecto académico · FastAPI · 2025
