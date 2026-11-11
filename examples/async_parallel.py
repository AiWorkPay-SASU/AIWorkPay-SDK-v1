"""Commander plusieurs missions en parallèle et attendre toutes les livraisons."""

import asyncio
from datetime import datetime, timedelta, timezone

from aiworkpay import AsyncAIWorkPay


async def main() -> None:
    deadline = datetime.now(timezone.utc) + timedelta(days=1)
    async with AsyncAIWorkPay() as client:
        created = await asyncio.gather(
            *(
                client.create_mission(
                    title=f"Vérification n°{i}",
                    description="Vérifier l'adresse et envoyer une photo.",
                    budget=10,
                    deadline=deadline,
                    idempotency_key=f"exemple-parallele-{i}",
                )
                for i in range(1, 4)
            )
        )
        for c in created:
            print("À payer :", c.payment.url if c.payment else "(rien à payer)")
        missions = await client.wait_for_deliveries([c.mission.id for c in created], timeout=24 * 3600)
        for mission in missions:
            print(mission.id, mission.status, mission.result_note)


if __name__ == "__main__":
    asyncio.run(main())
