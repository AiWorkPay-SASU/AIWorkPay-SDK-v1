"""Commander une mission humaine, attendre le résultat, la valider.

    export AIWORKPAY_API_KEY=awp_...        # clé fournie par AIWorkPay
    export AIWORKPAY_BASE_URL=http://localhost:3000   # facultatif (recette locale)
    python examples/quickstart.py

Par défaut le paiement passe par Stripe Checkout : un humain doit ouvrir l'URL affichée.
Rien n'est débité par ce script. `approve_mission` paie le Payworker et est irréversible :
il n'est appelé qu'avec --approve.
"""
import sys
from datetime import datetime, timedelta, timezone

from aiworkpay import AIWorkPay, MissionCanceledError, WaitTimeoutError


def main() -> int:
    client = AIWorkPay()  # AIWORKPAY_API_KEY, AIWORKPAY_BASE_URL
    account = client.get_account()
    print("Plafond de la prochaine mission :", account.max_next_mission_budget)

    created = client.create_mission(
        title="Vérifier l'ouverture d'un commerce",
        description="Vérifier sur place que le commerce est ouvert et photographier la façade.",
        budget=20,
        deadline=datetime.now(timezone.utc) + timedelta(days=2),
        idempotency_key="exemple-quickstart-1",  # un rejeu ne crée pas une 2e mission
    )
    print("Mission :", created.mission.id)
    print("À payer par votre propriétaire :", created.payment.url if created.payment else "(rien à payer)")

    try:
        mission = client.wait_for_delivery(created.mission.id, timeout=2 * 24 * 3600)
    except (MissionCanceledError, WaitTimeoutError) as error:
        print("Pas de résultat :", error)
        return 1

    print("Résultat :", mission.result_note, mission.result_data)
    if "--approve" in sys.argv:
        client.approve_mission(mission.id)
        print("Mission validée, Payworker payé.")
    else:
        print("Relancez avec --approve pour valider, ou appelez request_changes().")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
