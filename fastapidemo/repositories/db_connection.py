from typing import Annotated

from psycopg_pool import AsyncConnectionPool
from fastapi import Depends

from .config import DatabaseConfig


async def connection_pool():
    config = DatabaseConfig()
    async with AsyncConnectionPool(
            conninfo=f"postgresql://{config.username}:{config.password}@{config.pg_host}:{config.port}/{config.db_name}",
            min_size=config.min_connections,
            max_size=config.max_connections,
            check=AsyncConnectionPool.check_connection
    ) as pool:
        yield pool

ConnectDeps = Annotated[AsyncConnectionPool, Depends(connection_pool)]
