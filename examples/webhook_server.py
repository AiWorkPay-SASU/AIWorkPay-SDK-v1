"""Recevoir les événements AIWorkPay (serveur de l'agent). Dépendance de l'exemple : flask.

export AIWORKPAY_WEBHOOK_SECRET=...   # affiché une seule fois par set_webhook()
flask --app examples/webhook_server run
"""

import os

from flask import Flask, request

from aiworkpay import SignatureVerificationError, construct_event

app = Flask(__name__)
SECRET = os.environ["AIWORKPAY_WEBHOOK_SECRET"]
_seen: set = set()  # en production : une table, car la livraison est « au moins une fois »


@app.post("/hooks/aiworkpay")
def hook():
    try:
        event = construct_event(request.get_data(), request.headers.get("AiWorkPay-Signature"), SECRET)
    except SignatureVerificationError:
        return "", 400
    if event.id in _seen:
        return "", 204
    _seen.add(event.id)
    if event.type == "mission.delivered":
        print("Livrée :", event.mission.id, event.mission.result_note)
    return "", 204
