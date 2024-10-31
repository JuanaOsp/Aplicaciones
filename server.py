"""Python Flask WebApp Auth0 integration example
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from auth0_utils import update_user_metadata  # Importa la función desde auth0_utils

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Controllers API
@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


# Nuevo endpoint para manejar el formulario y actualizar user_metadata
@app.route("/submit_form", methods=["POST"])
def submit_form():
    user_id = session["user"]["userinfo"]["sub"]  # Obtener el ID del usuario en Auth0
    data = {
        "tipoDocumento": request.form["tipoDocumento"],
        "numeroDocumento": request.form["numeroDocumento"],
        "direccion": request.form["direccion"],
        "telefono": request.form["telefono"]
    }

    try:
        response = update_user_metadata(user_id, data)
        if response.get("error"):
            raise Exception(response["error"])
        return redirect(url_for("home"))  # Redirige a la página principal o perfil
    except Exception as e:
        print(f"Error al actualizar user_metadata: {e}")  # Muestra el error en la consola
        return f"Error actualizando datos: {e}", 500  # Muestra el error en la respuesta HTTP


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000), debug=True)
