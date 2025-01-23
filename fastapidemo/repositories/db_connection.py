from typing import Annotated

import psycopg
from fastapi import Depends
from psycopg import Connection

from .config import DatabaseConfig


async def connect():
    config = DatabaseConfig()
    async with await psycopg.AsyncConnection.connect(
            f'host={config.pg_host} '
            f'port={config.port} '
            f'dbname={config.db_name} '
            f'user={config.username} '
            f'password={config.password}'
    ) as conn:
        yield conn


ConnectDeps = Annotated[Connection, Depends(connect)]
