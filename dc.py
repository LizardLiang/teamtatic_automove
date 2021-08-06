# -*- coding: utf-8 -*-
import os
import discord
from dotenv import load_dotenv

from flask import Flask
from flask import request
import threading
import json
import requests
import webbrowser
import asyncio

from rauth import OAuth2Service

load_dotenv()
access_token = ""
auth_url = "https://discordapp.com/api/users/@me"

app = Flask(__name__)


def get_id(token):
    bearer = "Bearer " + token
    res = requests.get(auth_url, headers={"Authorization": bearer})

    data = json.loads(res.text)
    id = data["id"]

    res = requests.post("http://localhost:8091/auth", json={"id": id})
    data = json.loads(res.text)
    res = data["result"]
    
    if res == "Success":
        pass


@app.route("/")
def get_token():
    # Get code from return
    code = request.args.get("code")

    # Post to token_url to get token
    res = requests.post(
        "https://discordapp.com/api/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8090",
        },
        verify=False,
        allow_redirects=False,
        auth=(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")),
    )

    # Response is application/json
    data = json.loads(res.text)
    token = data["access_token"]

    # Use token to get user info
    res = get_id(token)
    return res


def Run_Server():
    server_thread = threading.Thread(
        target=app.run, daemon=True, kwargs={"host": "0.0.0.0", "port": 8090}
    )

    server_thread.start()


# @app.route("/auth")
# def auth():
#     content = request.json

#     if "code" in content:


def Start_Auth():
    service = OAuth2Service(
        name="Discord",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        access_token_url="https://discordapp.com/api/oauth2/token",
        authorize_url="https://discordapp.com/api/oauth2/authorize",
        base_url="https://discordapp.com/",
    )

    params = {
        "scope": "identify",
        "redirect_url": "http://localhost:8090",
        "grant_type": "authorization_code",
        "response_type": "code",
    }
    session = service.get_authorize_url(**params)

    webbrowser.register(
        "chrome",
        None,
        webbrowser.BackgroundBrowser(
            "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"
        ),
    )
    webbrowser.open(session, new=0, autoraise=True)
