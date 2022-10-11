from main import app
from schemas import IMatchs
from crud import MatchService


@app.get("/matchs")
def read_matchs():
    result = MatchService.read_matchs()
    return result


@app.get("/match/{id_match}")
async def read_match(id_match: int):
    try:
        result = MatchService.read_match(id_match)
    except:
        result = "error"
    return result


@app.post("/match/add")
def create_match(match: IMatchs.Match_create):
    try:
        MatchService.create_match(match)
    except Exception as e:
        return {"error": e}
    return "Match added succesfully"
