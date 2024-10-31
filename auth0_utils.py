# auth0_utils.py
import requests
from os import environ as env

def get_auth0_token():
    url = f"https://{env.get('AUTH0_DOMAIN')}/oauth/token"
    payload = {
        "client_id": env.get("AUTH0_CLIENT_ID"),
        "client_secret": env.get("AUTH0_CLIENT_SECRET"),
        "audience": f"https://{env.get('AUTH0_DOMAIN')}/api/v2/",
        "grant_type": "client_credentials"
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Agrega manejo de errores
    return response.json().get("access_token")

def update_user_metadata(user_id, data):
    url = f"https://{env.get('AUTH0_DOMAIN')}/api/v2/users/{user_id}"
    token = env.get("AUTH0_API_TOKEN")  # Este token debe ser válido y con permisos correctos

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
        print(f"Error de solicitud: {e}")  # Log el error
        raise Exception(f"Error al actualizar user_metadata: {e}")

    return response.json()