## Devolución de datos

Al consumir "/match/add":

* En caso de que la partida sea agregada

```json
{
  "Status": "Match added succesfully"
}
```

**

## Respuestas con manejo de errores

Se listará a continuación las posibilidades de devoluciones para errores en cada campo.
Luego errores conjuntos de dichas posibilidades devolverá la concatenación de esas devoluciones individuales.

### En caso de que no sea agregada porque el nombre es vacío

**Pedido**

```json
{
  "name": "",
  "max_players": 4,
  "min_players": 2,
  "password": "string",
  "n_matchs": 100,
  "n_rounds_matchs": 10
}
```
**Respuesta**

Status = 422 Error: Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "name"
      ],
      "msg": "El nombre no puede ser vacío",
      "type": "value_error"
    }
  ]
}
```

**

### En caso de que no sea agregada porque el nombre son caracteres vacíos

**Pedido**

```json
{
  "name": " ",
  "max_players": 4,
  "min_players": 2,
  "password": "string",
  "n_matchs": 100,
  "n_rounds_matchs": 10
}
```
**Respuesta**

Status = 422 Error: Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "name"
      ],
      "msg": "El nombre no puede contener caracteres vacíos",
      "type": "value_error"
    }
  ]
}
```

**

## Casos de entradas numéricas

Se toma el abs de todas las entradas, por lo que si queremos ingresar:

> n_matchs = -32

Tendremos 32 número de rondas, así para todos los atributos numéricos.
Para cada entrada se chequea el rango.
Se toman los:

> min(abs(match.n_matchs), 200)

> min(abs(match.n_rounds_matchs), 10000)

No se pueden ingresar Strings porque se realizan chequeos de tipo. 

### En caso de que no sea agregada porque max_players no está en I = { 2, 3, 4 } 

**Pedido**

```json
{
  "name": "partida1",
  "max_players": 5,
  "min_players": 2,
  "password": "string",
  "n_matchs": 100,
  "n_rounds_matchs": 10
}
```
**Respuesta**

Status = 422 Error: Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "max_players"
      ],
      "msg": "El valor debe estar entre 2 y 4",
      "type": "value_error"
    }
  ]
}
```

**

### En caso de que no sea agregada porque min_players no está en I = { 2, 3, 4 } 

**Pedido**

```json
{
  "name": "partida1",
  "max_players": 4,
  "min_players": 5,
  "password": "string",
  "n_matchs": 100,
  "n_rounds_matchs": 10
}
```
**Respuesta**

Status = 422 Error: Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "min_players"
      ],
      "msg": "El valor debe estar entre 2 y 4",
      "type": "value_error"
    }
  ]
}
```

**

### En caso de que no sea agregada porque min_players no está en I = { 2, 3, 4 } 

**Pedido**

```json
{
  "name": "partida1",
  "max_players": 4,
  "min_players": 5,
  "password": "string",
  "n_matchs": 100,
  "n_rounds_matchs": 10
}
```
**Respuesta**

Status = 422 Error: Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "min_players"
      ],
      "msg": "El valor debe estar entre 2 y 4",
      "type": "value_error"
    }
  ]
}
```


**

### En caso de que no sea agregada porque n_match no está en I = { 1, 2, 3, ..., 200 } 

**Pedido**

```json
{
  "name": "partida1",
  "max_players": 4,
  "min_players": 2,
  "password": "string",
  "n_matchs": 201,
  "n_rounds_matchs": 10
}
```
**Respuesta**

Status = 422 Error: Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "n_matchs"
      ],
      "msg": "El valor debe estar entre 1 y 200",
      "type": "value_error"
    }
  ]
}
```

**

### En caso de que no sea agregada porque n_rounds_matchs no está en I = { 1, 2, 3, ..., 10.000 } 

**Pedido**

```json
{
  "name": "partida1",
  "max_players": 4,
  "min_players": 2,
  "password": "string",
  "n_matchs": 200,
  "n_rounds_matchs": 0
}
```
**Respuesta**

Status = 422 Error: Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "n_rounds_matchs"
      ],
      "msg": "El valor debe estar entre 2 y 10.000",
      "type": "value_error"
    }
  ]
}
```

**

### En caso que falte algún campo solicitado

**Pedido**

```json
{
  "name": "partida1",
  "max_players": 4,
  "min_players":  ,         // <---
  "password": "string",
  "n_matchs": 200,
  "n_rounds_matchs": 0
}
```
**Respuesta**

Status = 422 Error: Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": [
        "body",
        62
      ],
      "msg": "Expecting value: line 4 column 19 (char 62)",
      "type": "value_error.jsondecode",
      "ctx": {
        "msg": "Expecting value",
        "doc": "{\n  \"name\": \"partida1\",\n  \"max_players\": 4,\n  \"min_players\":  ,\n  \"password\": \"string\",\n  \"n_matchs\": 200,\n  \"n_rounds_matchs\": 0\n}",
        "pos": 62,
        "lineno": 4,
        "colno": 19
      }
    }
  ]
}
```