"""
Serveur MCP météo — utilise wttr.in (API publique, sans clé API requise).
Usage : python mcp_meteo.py
Dépendances : pip install mcp httpx
"""

import asyncio
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("meteo-server")


async def _fetch_weather(city: str) -> dict:
    """Appelle wttr.in en format JSON."""
    url = f"https://wttr.in/{city}?format=j1"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description=(
                "Retourne les conditions météo actuelles d'une ville. "
                "Données : température (°C), ressenti, description, humidité, vent (km/h)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nom de la ville en anglais ou français (ex: Paris, Tokyo, Lyon)",
                    }
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="get_forecast",
            description=(
                "Retourne les prévisions météo sur 1 à 3 jours pour une ville. "
                "Données par jour : température min/max, description, précipitations."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nom de la ville",
                    },
                    "days": {
                        "type": "integer",
                        "description": "Nombre de jours de prévision (1, 2 ou 3)",
                        "minimum": 1,
                        "maximum": 3,
                    },
                },
                "required": ["city"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    city = arguments.get("city", "")

    if not city or not city.replace(" ", "").replace("-", "").isalpha():
        return [TextContent(
            type="text",
            text=f"Erreur : '{city}' n'est pas un nom de ville valide. "
                 "Utilisez uniquement des lettres (ex: Paris, New-York).",
        )]

    try:
        data = await _fetch_weather(city)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return [TextContent(
                type="text",
                text=f"Ville inconnue : '{city}'. Vérifiez l'orthographe (utilisez le nom anglais si possible).",
            )]
        return [TextContent(type="text", text=f"Erreur API météo (HTTP {e.response.status_code}).")]
    except httpx.TimeoutException:
        return [TextContent(type="text", text="Délai dépassé. L'API météo ne répond pas. Réessayez dans quelques instants.")]
    except Exception as e:
        return [TextContent(type="text", text=f"Erreur inattendue : {e}")]

    if name == "get_weather":
        current = data["current_condition"][0]
        result = {
            "ville": city,
            "temperature_c": int(current["temp_C"]),
            "ressenti_c": int(current["FeelsLikeC"]),
            "description": current["weatherDesc"][0]["value"],
            "humidite_pct": int(current["humidity"]),
            "vent_kmh": int(current["windspeedKmph"]),
            "direction_vent": current["winddir16Point"],
            "visibilite_km": int(current["visibility"]),
        }
        lignes = [
            f"Météo actuelle — {city}",
            f"  Température : {result['temperature_c']}°C (ressenti {result['ressenti_c']}°C)",
            f"  Conditions  : {result['description']}",
            f"  Humidité    : {result['humidite_pct']}%",
            f"  Vent        : {result['vent_kmh']} km/h {result['direction_vent']}",
            f"  Visibilité  : {result['visibilite_km']} km",
        ]
        return [TextContent(type="text", text="\n".join(lignes))]

    if name == "get_forecast":
        days = min(int(arguments.get("days", 3)), 3)
        forecasts = data["weather"][:days]
        lignes = [f"Prévisions météo — {city}"]
        for day in forecasts:
            date = day["date"]
            tmin = day["mintempC"]
            tmax = day["maxtempC"]
            desc = day["hourly"][4]["weatherDesc"][0]["value"]
            precip = day["hourly"][4]["precipMM"]
            lignes.append(
                f"  {date} : {tmin}°C → {tmax}°C, {desc}, précip. {precip}mm"
            )
        return [TextContent(type="text", text="\n".join(lignes))]

    return [TextContent(type="text", text=f"Outil inconnu : {name}")]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
