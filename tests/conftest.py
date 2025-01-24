import os
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from psycopg_pool import AsyncConnectionPool
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer

from fastapidemo.main import app
from fastapidemo.repositories.db_connection import connection_pool

PGIMAGE = "postgres:15.10"
PGUSER = "demo"
PGPASS = "demop"
PGDB = "demo"
PGPORT = 5432
MIN_SIZE = 2
MAX_SIZE = 3


def _connection_pool():
    port = os.getenv('PGPORT', "5432")
    return AsyncConnectionPool(
        conninfo=f"postgresql://{PGUSER}:{PGPASS}@localhost:{port}/{PGDB}",
        min_size=MIN_SIZE,
        max_size=MAX_SIZE,
        check=AsyncConnectionPool.check_connection
    )


@pytest.fixture(scope="session")
def postgres_container():
    postgres = PostgresContainer(
        image=PGIMAGE,
        username=PGUSER,
        password=PGPASS,
        dbname=PGDB,
        port=PGPORT
    )
    with postgres:
        wait_for_logs(
            postgres,
            r"UTC \[1\] LOG:  database system is ready to accept connections",
            10,
        )
        yield postgres


@pytest.fixture(scope="session")
async def db_pool(postgres_container):
    os.environ["PGPORT"] = str(postgres_container.get_exposed_port(port=PGPORT))
    async with _connection_pool() as pool:
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(open(Path(__file__).parent.parent.joinpath("sql/init-schema.sql"), 'r').read())
        yield pool


@pytest.fixture(scope="module")
async def test_client(db_pool):
    app.dependency_overrides[connection_pool] = lambda: db_pool
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(scope="function", autouse=True)
async def empty_db(db_pool):
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM demo.contacts CASCADE")
            await cur.execute("DELETE FROM demo.courses CASCADE")


@pytest.fixture(scope="function")
async def create_course(db_pool):
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO demo.courses(name, subject, start_date)
                VALUES ('Intro to quantum mechanics', 'Physics', '2025-02-01')
                """
            )
