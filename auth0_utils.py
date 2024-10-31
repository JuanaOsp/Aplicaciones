import requests
from os import environ as env

def update_user_metadata(user_id, data):
    url = f"https://{env.get('AUTH0_DOMAIN')}/api/v2/users/{user_id}"
    token = env.get("AUTH0_API_TOKEN")  # Asegúrate de que este token tenga permisos

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "user_metadata": data
    }

    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
    except requests.exceptions.RequestException as e:
        print(f"Error de solicitud: {e}")  # Log del error
        raise Exception(f"Error al actualizar user_metadata: {e}")

    return response.json()
