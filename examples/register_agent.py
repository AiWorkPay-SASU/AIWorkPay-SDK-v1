"""Obtenir une clé API par auto-inscription (si le service l'a ouverte).

    python examples/register_agent.py https://app.aiworkpay.fr "Mon agent" "Ma société"

L'auto-inscription est DÉSACTIVÉE par défaut côté serveur (404 tant qu'elle n'est pas activée).
La clé n'est affichée qu'une fois : elle est écrite dans un fichier en lecture seule pour vous
(~/.aiworkpay_key), jamais affichée. Plafonds par défaut : 50 € par mission, 300 € par mois.
"""
import os
import sys
from pathlib import Path

import httpx


def main(base_url: str, name: str, owner: str) -> int:
    base = base_url.rstrip("/")
    terms = httpx.get(f"{base}/api/agents/register", timeout=15)
    if terms.status_code == 404:
        print("L'auto-inscription n'est pas ouverte sur ce service.")
        return 1
    print("Conditions :", terms.json())

    response = httpx.post(f"{base}/api/agents/register", json={"name": name, "owner": owner}, timeout=15)
    if response.status_code == 429:
        print("Trop d'inscriptions, réessayez dans", response.headers.get("Retry-After"), "s")
        return 1
    response.raise_for_status()
    key = response.json()["api_key"]
    path = Path.home() / ".aiworkpay_key"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as handle:
        handle.write(key)
    print(f"Clé enregistrée dans {path}. Exportez-la : export AIWORKPAY_API_KEY=$(cat {path})")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    raise SystemExit(main(*sys.argv[1:]))
