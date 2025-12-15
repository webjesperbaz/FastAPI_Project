### User schema ###     # Clase en vídeo (22/12/2022): https://www.twitch.tv/videos/1686104006

def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]}


def users_schema(users) -> list:                    #Indica que la función debería devolver un valor de tipo list. No afecta al comportamiento del código, pero ayuda a quien lo lee y a las herramientas de desarrollo a entender el tipo de dato que se espera como salida.
    return [user_schema(user) for user in users]    #Se lee así: "Devuelve una nueva lista, donde cada elemento es el resultado de llamar a user_schema(user) para cada user dentro de la lista original users."

