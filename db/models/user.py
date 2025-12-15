from pydantic import BaseModel

class User(BaseModel):
    id: str | None      #pongo none porque puede que no se le pase, ya mongodb al introducir usuario le cre un indice
    username: str
    email: str
    