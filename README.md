# Becarfuliate Back
Repositorio backend para ingeniería del software

## Instalación y creación base de datos

### Requerimientos

> pip install -r requeriments.txt

Luego seguir los pasos instalando [SQLite3](#instalación-sqlite-3)

### Instalación SQLite 3

Después de realizar eso, lo segundo que deben hacer es crear la base de datos en *sqlite 3*.

```
$ sudo apt-get update
$ sudo apt-get install sqlite3
$ sqlite3 --version
$ sudo apt-get install sqlitebrowser
```

## Levantar fastapi

Una vez realizado todo, pueden levantar el servidor de fastapi de esta manera

```
$ uvicorn app:app --reload
```
y una vez levantado ingresan a: 

http://127.0.0.1:8000/docs 

o a 

http://127.0.0.1:8000/redoc


## Configurar VSCode con black linter y pep8

Tutorial original [aca](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0).

En VSCode descargar la extensión de python en la barra de extensiones

Una vez instalada, ir a settings y buscar "python formatting provider", en el resultado elegir la opción "black"

Una vez elegido, buscar "Format on save" y tildar la opción.


## Otros

### Creación entorno virtual

Antes de arrancar debemos crear un **entorno virtual**, para instalar todos los *packages* que se utilizarán en este proyecto. 

```sh
$ sudo apt-get install virtualenv
$ virtualenv -p /usr/bin/python3 <nombre>
$ source <nombre>/bin/activate
```

**Desactivar venv**
```sh
# En el path donde esté el venv.
$ deactivate
```

### Paquetes instalados en el venv

Una vez en el entorno deben instalar los *packages* necesarios (fastapi, ponyorm, sqlite)

```
$ pip install fastapi
$ pip install "uvicorn[standard]"
$ pip install pony 
$ pip install black
```

### Formato

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

### Devolución de datos

Al consumir "/matchs"
```json
[
    {
        "name":"partiduela",
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
    "name":"partiduela",
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
"error"
```


Al consumir "/match/add":

* En caso de que la partida sea agregada

```json
"Match added succesfully"
```

* En caso de que no sea agregada

```json
{
  "error": {
    "original_exc": {
      "original_exc": {}
    }
  }
}
```