import itertools
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException

from model import FootballMatch, MatchCreate, MatchUpdate

app = FastAPI()
app.state.matches = []
app.state.id_generator = itertools.count(1)


# Получение всех матчей
@app.get("/matches/", response_model=List[FootballMatch])
def get_matches():
    return app.state.matches


# Получение матча по ID
@app.get("/matches/{match_id}", response_model=FootballMatch)
def get_match_by_id(match_id: int):
    match = next((m for m in app.state.matches if m.id == match_id), None)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


# Добавление нового матча
@app.post("/matches/", response_model=FootballMatch)
def create_match(match: MatchCreate):
    new_id = next(app.state.id_generator)
    new_match = FootballMatch(id=new_id, **match.model_dump())
    app.state.matches.append(new_match)
    return new_match


# Сортировка матчей по полю
@app.get("/matches/sort/", response_model=List[FootballMatch])
def get_sorted_matches(field: str, order: str = "asc"):
    if field not in [
        "home_team",
        "away_team",
        "home_score",
        "away_score",
        "match_date",
        "place",
        "duration",
        "yellow_cards",
        "red_cards",
    ]:
        raise HTTPException(status_code=400, detail="Invalid field")

    reverse = order == "desc"
    sorted_matches = sorted(
        app.state.matches, key=lambda x: getattr(x, field), reverse=reverse
    )
    return sorted_matches


# Получение статистики по числовым полям
@app.get("/matches/stats/")
def get_stats(field: str):
    if field not in [
        "home_score",
        "away_score",
        "duration",
        "yellow_cards",
        "red_cards",
    ]:
        raise HTTPException(status_code=400, detail="Invalid field")

    values = [getattr(match, field) for match in app.state.matches]
    avg_val = sum(values) / len(values) if values else 0
    max_val = max(values) if values else None
    min_val = min(values) if values else None

    return {"average": avg_val, "max": max_val, "min": min_val}


# Обновление матча по id
@app.put("/matches/{match_id}")
def update_match(match_id: int, match: MatchUpdate):
    for i, m in enumerate(app.state.matches):
        if m.id == match_id:
            update_data = match.model_dump(exclude_unset=True)
            updated_match = m.model_copy(update=update_data)
            app.state.matches[i] = updated_match
            return updated_match
    raise HTTPException(status_code=404, detail="Match not found")


# Удаление матча по id
@app.delete("/matches/{match_id}")
def delete_match(match_id: int):
    match = next((m for m in app.state.matches if m.id == match_id), None)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    app.state.matches.remove(match)
    return {"detail": "Match deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
