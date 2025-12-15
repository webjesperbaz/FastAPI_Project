# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480)

### MongoDB client ###

# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# Módulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost

from pymongo import MongoClient

#CONEXION BADE DATOS EN LOCAL:
# db_client= MongoClient().local    # creo una instancia de conexion. 
                            # Es importante que sepamos que si es en local es (), pero si me conectase a una bd en remoto, dentro de lao corchetes iria la url.

#CONEXION BASE DE DATOS REMOTA:                                                                                             #nombre db en remotp
db_client= MongoClient("mongodb+srv://webjesperbaz_db_user:bwkWAtP0gjHDPFzw@cluster0.tmmd5tl.mongodb.net/?appName=Cluster0").test
                        #URL a la que se conectará. Pero nosotros no tenemos que cambiar el localhostm ya que se conectará a esta.