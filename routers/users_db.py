### USERS DB API ###  fichero para manejar las entodades que utilicemos

from fastapi import APIRouter, HTTPException, status     ### impotación de fastapi ###
from db.models.user import User                  #importamos el modelo user
from db.schemas.user import user_schema, users_schema
from db.client import db_client                  #importamos el cliente de la bd, que es la conexion a la bd
from pymongo.collection import Collection
from bson import ObjectId

router = APIRouter(prefix="/userdb",         ### instancia de APIRouter ###
                    tags=["userdb"],        # para qie en la documentacion lo meta ya en userdb    
                responses={status.HTTP_404_NOT_FOUND: {"message": "no encontrado"}})                       
                


# levanta el servidor local: uvicorn users:app --reload
# Url local: http://127.0.0.1:8000



##################################### GET --> TRAER INFORMACION #############################################################

@router.get("/", response_model=list[User])  #devielve todos los users de la db
async def users():
	return users_schema(db_client.users.find())   #importante, hay que darle formato o schema a la busqueda



@router.get("/{id}")  # Path
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/")  # Query
async def user(id: str):
    return search_user("_id", ObjectId(id))


    ####################################### POST --> insertar datod en la bd #############################################################
    

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)		# insertar un usuario          
async def user(user: User):
    
    #lo comprueba si existe:
    if type (search_user("email", user.email)) == User:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    else:   #si no existe, lo guardo:	
        user_dic = dict(user)   #tambien funciona: user.model_dump()		#lo que meto lo paso a diccionario, ya que mongodb trabaja con json que son dinccionarios
    
        del user_dic["id"]			#borro el id para que solo coca ls demas datos, ya que mongodb ya crea los indices por si mismo
    
        id = db_client.users.insert_one(user_dic).inserted_id       #esto, guarda 
        #conex bd  donde	esquema	inserto1  tipo	inserta un id
        new_user = user_schema(db_client.users.find_one({"_id": id}))		#Recuperar: usamos la funcion para transformar el json en la clase cliente para mostrarlo

        return User(**new_user)	#creamos un tipo User, para mostrar

    





#:
#     if user in users_list:
#         return HTTPException(status_code=204, detail="usuario ya existe")       #para lanzar excepciones
#         # raise HTTPException(status_code=204, detail="usuario ya existe")      #para lanzar excepciones en el estado, mas profesional
#         # return {"usuario" : "ya existe"}                                      #para lanzar mensaje personal, menos profesional.
#     else:
#         users_list.append(user) 

#         return user         


    ####################################### PUT --> ACTUALIZAR #############################################################

                    #va aretotnar un usuario
@router.put("/", response_model=User)                   
async def user(user: User):

    user_dic = dict(user) 		#lo que meto lo paso a diccionario, ya que mongodb trabaja con json que son dinccionarios
    del user_dic["id"]          #por que no queremos que actualicd el campo id
    
    try:
        found= db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dic)        
                #2º actualizacion                           #busqueda de id       ,  lo que guardo
    except:
        return {"error": "no se ha actualizado el usuario"}

    return search_user({"_id": ObjectId(user.id)})
          
        


    ####################################### eliminar #############################################################



@router.delete("/{id}" )                   
async def user(id: str):
    
     found= db_client.users.find_one_and_delete({"_id": ObjectId(id)})  #1º busco al ausuario que quiero borrar
    
     if not found: 
        return {"error":"no se ha borrado el usuario"}
                      

        



        ################################# funciones de apoyo #############################################


def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}





#git 1