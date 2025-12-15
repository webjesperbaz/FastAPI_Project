# Clase en vídeo: https://youtu.be/_y9qQZXE24A

# Documentación oficial: https://fastapi.tiangolo.com/es/

# Instala FastAPI: pip install "fastapi[all]"


from fastapi import FastAPI     ### impotación de fastapi ###
# from Backend.FastAPI.routers import users_db
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles  ### para poder ver archivos estáticos ###


app = FastAPI()                 ### instancia de fastapi ###

#Routers
app.include_router(products.router)   ### incluir los otros archivos ###
app.include_router(users.router)      ### idem ###
app.include_router(basic_auth_users.router)      ### idem ###
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")        ### para montar archivos estaticos ###
            #ruta,     tipo,                            nombre


# levanta el servidor local: uvicorn main:app --reload
# Url local: http://127.0.0.1:8000

@app.get("/")                   ### ruta raiz del proyecto ###
async def root():               ### función que realiza al ser metida la direción ###
    return "¡Hola FastAPI!" 

@app.get("/url")                   
async def url():              
    return { "url":"https://mouredev.com/python" }         #json con la url del curso#



# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc