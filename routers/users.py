from fastapi import APIRouter, HTTPException     ### impotación de fastapi ###
from pydantic import BaseModel  ### para crear entidades ###

router = APIRouter(prefix="/user")                 ### instancia de APIRouter ###

# levanta el servidor local: uvicorn users:app --reload
# Url local: http://127.0.0.1:8000


# entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list= [User (id=1, name= "Brais", surname= "Moure", url="https://moure.dev", age= 35),
             User (id=2, name= "Moure", surname= "Dev", url="https://moure.dev", age= 35),
             User (id=3, name= "Jesus", surname= "Perea", url="https://moure.dev", age= 39)]


 ##################################### GET --> TRAER INFORMACION #############################################################


@router.get("/json")                   
async def usersjson():              
    return  [{"name": "Brais", "surname": "noure", "url": "https://moure.dev", "age": 35},
             {"name": "Moure", "surname": "Dev", "url": "https://moure.dev", "age": 35},
             {"name": "Jesus", "surname": "Perea", "url": "https://moure.dev", "age": 39}]


@router.get("/oll")                   
async def users():              
    return users_list


@router.get("/{id}")                 ###filtrar usuarios por id, o PATH###       
async def user(id: int):
    
    users= filter(lambda user: user.id == id, users_list)
     
    try:         
        return list(users)[0]
    except:
        return {"chunguele...": "usuario no encontrado"}
    
    

@router.get("/query/")                 ###filtrar usuarios por QUERY....ej:  url/?id=1  ###       
async def user(id: int):
    
    users= filter(lambda user: user.id == id, users_list)
     
    try:         
        return list(users)[0]
    except:
        return {"chunguele...": "usuario no encontrado"}
    

    ####################################### POST --> AÑADIR #############################################################
    

@router.post("/create", status_code=201)                          # status_code=, es para mostrar errores genericos             
async def user(user: User):
    if user in users_list:
        return HTTPException(status_code=204, detail="usuario ya existe")       #para lanzar excepciones
        # raise HTTPException(status_code=204, detail="usuario ya existe")      #para lanzar excepciones en el estado, mas profesional
        # return {"usuario" : "ya existe"}                                      #para lanzar mensaje personal, menos profesional.
    else:
        users_list.append(user) 

        return user         
    

    ####################################### PUT --> ACTUALIZAR #############################################################


@router.put("/put")                   
async def user(user: User):
    for index, save_user in enumerate(users_list):        ### si el usuario guardado esta en la lista, la tenemos que enumerar ###
        if save_user.id == user.id:     ### si la id del usuario guardado está en la lista ###
            users_list[index] = user

            return user , {"actualizado correctamente"}
        


        ####################################### PUT --> ACTUALIZAR #############################################################



@router.delete("/delete/{id}")                   
async def user(id: int):
    for index, borrar_usu in enumerate(users_list):
        if borrar_usu.id == id:
           del users_list[index]

        return {"borrado realizado"}