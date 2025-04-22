# UEFA Players API - Proyecto FastAPI

Este proyecto es una API construida con **FastAPI** que gestiona metricas y compara los jugadores del FIFA 2022 con los jugadores de fútbol de la (temporada UEFA 2021-22). 

---

## 🚀 Características principales

- Gestión de **jugadores** y **players** como modelos independientes.
- CRUD completo para ambos modelos (`GET`, `POST`, `PUT`, `DELETE`).
- Exportación de datos a archivos `.csv`.
- Filtros dinámicos:
  - Filtrar jugadores por país.
  - Filtrar players por valor de `overall`.
- Eliminación lógica en el modelo `Player` (trazabilidad con `is_active`).
- Separación del código por responsabilidades (`crud_*.py`, `main.py`, `player.py`, etc.).

---

## 📂 Estructura del proyecto

```
uefa2021-22/
├── main.py              # Punto de entrada de la aplicación FastAPI
├── database.py          # Conexión, modelos y setup de la base de datos
├── crud_jugador.py      # Funciones CRUD para Jugadores
├── crud_player.py       # Funciones CRUD para Players
├── jugador.py           # Pydantic model para Jugador
├── player.py            # Pydantic model para Player
├── players.csv          # Archivo de exportación para Players
├── jugadores.csv        # Archivo de exportación para Jugadores
└── uefa.db              # Base de datos SQLite asincrónica
```

---

## 🧭 Mapa de Endpoints

### 🔹 Endpoints generales
- `GET /` → Mensaje de bienvenida
- `GET /hello/{name}` → Saludo personalizado

### 🔹 Endpoints Jugadores (`JUGADORES`)
- `GET /jugadores` → Listar todos los jugadores
- `GET /jugadores/{sofifa_id}` → Obtener jugador por ID
- `POST /jugadores` → Crear nuevo jugador
- `PUT /jugadores/{sofifa_id}` → Actualizar jugador
- `DELETE /jugadores/{sofifa_id}` → Eliminar jugador
- `GET /jugadores/filtrar/pais/{pais}` → Filtrar jugadores por país
- `GET /jugadores1/export` → Exportar jugadores a `jugadores.csv`

### 🔹 Endpoints Players (`PLAYERS`)
- `GET /players` → Listar todos los players
- `GET /players/{sofifa_id}` → Obtener player por ID
- `POST /players` → Crear nuevo player
- `PUT /players/{sofifa_id}` → Actualizar player
- `DELETE /players/{sofifa_id}` → Eliminar player con trazabilidad
- `GET /players/filter/overall?min_overall=` → Filtrar por `overall`
- `GET /players1/export` → Exportar players a `players.csv`
- `GET /players1/eliminados` → Ver players eliminados (`is_active=False`)

---

## 🛠️ Requisitos y ejecución

### Requisitos
- Python 3.11+
- Dependencias: `fastapi`, `uvicorn`, `sqlalchemy`, `aiosqlite`, `pandas`

### Instalación y ejecución
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
```

### Acceso a la documentación interactiva
- 📘 [Swagger UI](http://127.0.0.1:8003/docs)

---

## 🧑‍💻 Autor
**Julian Buitrago Camacho**  
Proyecto académico FastAPI 2025


