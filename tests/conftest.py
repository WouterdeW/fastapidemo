import os
from pathlib import Path

import pytest
import psycopg
from httpx import AsyncClient, ASGITransport
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer

from fastapidemo.main import app
from fastapidemo.repositories.db_connection import connect

PGIMAGE = "postgres:15.10"
PGUSER = "demo"
PGPASS = "demop"
PGDB = "demo"
PGPORT = 5432


def _connect():
    port = os.getenv('PGPORT', "5432")
    return psycopg.AsyncConnection.connect(
        f'host=localhost '
        f'port={port} '
        f'dbname={PGDB} '
        f'user={PGUSER} '
        f'password={PGPASS}'
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
async def db(postgres_container):
    os.environ["PGPORT"] = str(postgres_container.get_exposed_port(port=PGPORT))
    async with await _connect() as conn:
        async with conn.cursor() as cur:
            await cur.execute(open(Path(__file__).parent.parent.joinpath("sql/init-schema.sql"), 'r').read())
        yield conn


@pytest.fixture(scope="module")
async def test_client(db):
    app.dependency_overrides[connect] = lambda: db
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(scope="function", autouse=True)
async def empty_db(db):
    async with db.cursor() as cur:
        await cur.execute("DELETE FROM demo.contacts CASCADE")
        await cur.execute("DELETE FROM demo.courses CASCADE")


@pytest.fixture(scope="function")
async def create_course(db):
    async with db.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO demo.courses(name, subject, start_date)
            VALUES ('Intro to quantum mechanics', 'Physics', '2025-02-01')
            """
        )
