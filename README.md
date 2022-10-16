### Formato utilizado

Install pylint
Luego: 
* File->Preferences->Settings 
* buscar "python formatting provider" elegir black. Por default estaba autopep8

Agregar en settings.json de vscode:

```json 
{
    "python.linting.pycodestyleEnabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "/home/<nombre>/.local/bin/black",
    "python.linting.pylintArgs": [
        "--max-line-length=180"
    ],
    "python.formatting.autopep8Args": [
        "--max-line-length=180"
    ],
    "editor.formatOnSave": true,
}
```

## Devolución de datos

Al consumir "/matchs"
```json
[
    {
        "name":"partida1",
        "max_players":0,
        "min_players":0,
        "password":"string",
        "n_matchs":0,
        "n_rounds_matchs":0,
        "id":0
    },
    {
      "name":"partida2",
      "max_players":0,
      "min_players":0,
      "password":"string",
      "n_matchs":0,
      "n_rounds_matchs":0,
      "id":1
    }
]
```

Al consumir "/match/{id}":

* En caso de que exista la partida:
```json
{
    "name":"partida1",
    "max_players":0,
    "min_players":0,
    "password":"string",
    "n_matchs":0,
    "n_rounds_matchs":0,
    "id":1
}
```

* En caso de que no exista la partida

```json
{
  "detail": "La partida no existe"
}
```
