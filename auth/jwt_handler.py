#este archivo es responsable de firmar,encodear,decodear y retornar JWT tokens
import time #necesario para setear tiempo de expiracion de tokens
import jwt #necesario para encodear y decodear tokens
from decouple import config #poder cambiar parametros sin tener que volver a levantar el back, los parametros se almacenan en env

#se obtienen de env
JWT_SECRET =config('secret')
JWT_ALGORITHM = config('algorithm')

#esta funcion devuelve los tokens generados
def token_response(token:str):
    return{
        "access token": token 
    }

#esta funcion encodea el token
def sign_JWT(userID:str):
    payload = {
        "userID" : userID,
        "expiry" : time.time()+600
    }
    token = jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return token_response(token)

#esta funcion decodea el token
def decode_JWT(token:str):
    try:
        decode_token = jwt.decode(token,JWT_SECRET,algorithm=JWT_ALGORITHM)
        if (decode_token['expires']>=time.time()):
            return decode_token
        else:None
    except:
        return{}
