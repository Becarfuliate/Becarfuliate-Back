from main import app
from schemas import IPartidas
from crud import PartidaService


@app.post("/partida/agregar")
def create_partida(partida: IPartidas.PartidaCreate):
    PartidaService.create_partida(partida)
    return "Se agregó la partida"
