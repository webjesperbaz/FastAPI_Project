from fastapi import  Depends, HTTPException, APIRouter, status
from pydantic import BaseModel  ### para crear entidades ###
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
                             # para aurenticacion           # mecanismo para capturar la contraseña(formulario)

router = APIRouter(prefix="/auth")

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "disabled": True,
        "password": "123456"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": False,
        "password": "654321"
    }
}

    

def search_userdb(username: str):         #funcion para buscar al usuario en la base de datos, segun lo que le pase
        if username in users_db:        
             return UserDB(**users_db[username])      #retorna el nombre del usuario si está en la "bd". Los dos asteriscos insican que pi¡ueden pasarle varios parametros
        

def search_user(username: str):         #funcion para buscar al usuario de tipo "User" en la base de datos, segun lo que le pase
        if username in users_db:        
             return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):           # criterio de dependencia, para que la condicion dependa de esto cuando sea usado
    user= search_user(token)
    if not user:
         raise HTTPException( status_code=401, detail="credenciales de autenticacion no valido")      #comprobar si lo ha encontrado o no
    
    if user.disabled:
          raise HTTPException( status_code=401, detail="Usuario inactivo")
    
    return user                                              
        

@router.post("/login")                     #operacion de autenticacion: 
async def login(form: OAuth2PasswordRequestForm = Depends()):  # form de tipo indicado para capturar los datos(usuario y contraseña)
     user_db = users_db.get(form.username)      #1º validamos usuario del formulario 
     if not user_db:
          raise HTTPException(status_code=400,detail="El usuario no e correcto")
     
     user= search_userdb(form.username)
     

     if not form.password == user.password:      # 2º Validamos la contraseña, comprobar si la contraseña que nos ha llegado tambien en el forulario, coincide tambien con el usuario
          raise HTTPException(status_code=400, detail="La contraseña no es correcta")
     
     return {"access_token": user.username, "token type": "bearer"}     #esto forma parte de un standard
                #defino que token elijo            3º genero un token


@router.get("/me")                       # una vez autenticado, esta funcion que me diga cual es mi usuario
async def me(user: User= Depends(current_user)):        #deberá cumplir el criterio de dependencia, este procedimiento funcionará si se cumple el depends
     return user