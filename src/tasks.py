from asyncio import run

from src.config import celery


@celery.task()
def ping():
    async def _ping():
        print("PONG")

    run(_ping())


@celery.task()
def pong():
    print("PING")
