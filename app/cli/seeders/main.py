import asyncio

import typer
from sqlalchemy.ext.asyncio import AsyncSession

from app.cli.seeders.topics.topic import seed_topics
from app.infrastructure.postgres.session import aget_session

app = typer.Typer(help="CLI tool for seeding the database with initial data.")


@app.command(help="Seed the topics table with initial data.")
def topics():
    async def seeding():
        async for db in aget_session():
            await seed_topics(db)

    asyncio.run(seeding())


if __name__ == "__main__":
    app()
