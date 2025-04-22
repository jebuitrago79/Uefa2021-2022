Mapa de Endpoints – UEFA 2021-22 API
🌐 General

    GET /
    Retorna un mensaje de bienvenida: {"message": "Hello World"}

    GET /hello/{name}
    Saludo personalizado con nombre.

⚽ Modelo: Jugador (modelo simplificado)

    GET /jugadores
    Obtener todos los jugadores.

    GET /jugadores/{sofifa_id}
    Obtener un jugador por su ID.

    POST /jugadores
    Crear un nuevo jugador.

    PUT /jugadores/{sofifa_id}
    Actualizar un jugador existente.

    DELETE /jugadores/{sofifa_id}
    Eliminar un jugador.

    GET /jugadores1/export
    Exportar todos los jugadores a CSV (jugadores.csv).

    GET /jugadores/filtrar/pais/{pais}
    Filtrar jugadores por nombre de país.

🏆 Modelo: Player (modelo extendido con métricas)

    GET /players
    Obtener todos los jugadores.

    GET /players/{sofifa_id}
    Obtener un jugador por ID.

    POST /players
    Crear un nuevo jugador (con métricas y trazabilidad).

    PUT /players/{sofifa_id}
    Actualizar datos de un jugador.

    DELETE /players/{sofifa_id}
    Eliminación lógica de un jugador (campo is_active = False).

    GET /players1/export
    Exportar todos los jugadores con métricas a CSV (players.csv).

    GET /players/filter/overall?min_overall=80
    Filtrar jugadores con un valor mínimo de overall.

    GET /players1/eliminados
    Listar jugadores que han sido eliminados lógicamente (is_active == False).
