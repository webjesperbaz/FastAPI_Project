
from fastapi import  FastAPI , Depends , HTTPException, APIRouter, status
from pydantic import BaseModel  ### para crear entidades ###
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
                             # para aurenticacion           # mecanismo para capturar la contraseña(formulario)
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta       # para calcular el tiempo de expiracion ddel token y trabajar con fechas

ALGORITHM= "HS256"
ACCESS_TOKEN_DURATION= 5            # duracion del token gerenado 1 min
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"  # numero secreto, da igual lo creamos nosotros

router = APIRouter(prefix="/authjwt")

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["sha256_crypt"], deprecated="auto")       #algoritmo de criptografia

# 1. Contraseña: 12345
#hash_mouredev = crypt.hash("123456")
#print(f"Hash para mouredev (123456): {hash_mouredev}")

# 2. Contraseña: 54321
#hash_mouredev2 = crypt.hash("654321")
#print(f"Hash para mouredev2 (654321): {hash_mouredev2}")


class User(BaseModel):      #user normal
    
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):         #user de la base de datos, hereda user y tiene lo mismo mas una contraseña
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "$5$rounds=535000$UDMkJnvkI2u/l2H2$cyB3ejnmAI2vkl6DeR6.bc7XMcq/g/9CuYdUY9C/QU9"      # 12345 la he creado con una web de crear bcrypt
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$5$rounds=535000$qHfB9Ajnbm.3Th6v$g61VpODI4IKqlzxGo.L69tPzML3fwtYnfLRH5qZebHB"      # 54321 la he creado con una web de crear bcrypt
    }
}

def search_userdb(username: str):         #funcion para buscar al usuario en la base de datos, segun lo que le pase
        if username in users_db:        
             return UserDB(**users_db[username])
        
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])       
        
async def auth_user(token: str = Depends(oauth2)):      #2º proceso para validar el token y encontrar al usuuario

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user                        


@router.post("/login")                     #1º operacion de autenticacion ó login: 
async def login(form: OAuth2PasswordRequestForm = Depends()):  # form de tipo indicado para capturar los datos(usuario y contraseña)
     user_db = users_db.get(form.username)      #1º validamos usuario del formulario 
     if not user_db:
          raise HTTPException(status_code=400,detail="El usuario no e correcto")
     
     user= search_userdb(form.username)

     password_to_check = form.password[:72].encode("utf-8")
                        #contraseña original == conytaseña en la  bd
     if not crypt.verify(password_to_check, user.password):      #2º verificamos si la contraseña introducida es la misma que la encriptada en la bd
          raise HTTPException(status_code=400, detail="La contraseña no es correcta")
     
                                                            

     #expire = datetime.now() + access_token_expiration      # ahora + tiempo de expiracion de un minuto despues de generarse
     access_token = {"sub": user.username,      #usuario
                    "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_DURATION)}       #tiempo de expiracion

     return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}# creamos un access token de manera segura
                #defino que token elijo   


    # Cómo usamos el token:               
@router.get("/me")     #3º operacion para saber mis datos ojo que el token expira en un minuto
async def me(user: User = Depends(current_user)):
      return user