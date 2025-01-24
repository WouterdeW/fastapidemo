import os
from pydantic.v1 import BaseSettings


class DatabaseConfig(BaseSettings):
    pg_host = os.getenv('PGHOST', '127.0.0.1')
    username = os.getenv('PGUSER', "demo")
    password = os.getenv('PGPW', "demop")
    port = os.getenv('PGPORT', "5432")
    db_name = "demo"
    min_connections = 2
    max_connections = 3

