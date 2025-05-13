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

## 🧱 Arquitectura general

```mermaid
flowchart TD
    subgraph Entrada_de_Datos["Entrada de Datos"]
        A1["CSV: Métricas FIFA 22"]
        A2["CSV: Estadísticas UEFA"]
    end

    subgraph Proceso_ETL["Proceso ETL"]
        B1["Limpieza y normalización\\n(pandas)"]
        B2["Unión de datasets\\npor nombre o ID"]
    end

    subgraph Persistencia["Persistencia"]
        C1["Modelos con SQLModel"]
        C2["Base de datos PostgreSQL\\n(Clever Cloud)"]
    end

    subgraph Backend_API["Backend API"]
        D1["FastAPI"]
        D2["Endpoints de comparación y análisis"]
        D3["Regresión y correlación\\n(statsmodels)"]
    end

    subgraph Visualizacion_y_Testing["Visualización y Testing"]
        E1["Postman o Navegador"]
        E2["Gráficas de resultados"]
    end

    subgraph Despliegue["Despliegue"]
        F1["Render.com - Backend"]
        F2["Clever Cloud - PostgreSQL"]
        F3["Repositorio GitHub"]
    end

    A1 --> B1
    A2 --> B1
    B1 --> B2
    B2 --> C1
    C1 --> C2
    C2 --> D1
    D1 --> D2
    D1 --> E1
    D1 --> F1
    D2 --> D3
    D2 --> E2
    F2 --> D1
    F3 --> D1
