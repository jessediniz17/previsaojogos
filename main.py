from fastapi import FastAPI
import requests

app = FastAPI()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.sofascore.com/",
}

@app.get("/team/{team_id}/last-games")
def last_games(team_id: int):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/0"
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        return {"error": "Erro ao acessar SofaScore"}

    return response.json()
