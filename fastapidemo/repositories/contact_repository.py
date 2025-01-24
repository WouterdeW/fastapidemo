from pydantic import EmailStr

from .db_connection import ConnectDeps
from ..models import UserType, Contact


class ContactRepository:
    def __init__(self, connection_pool: ConnectDeps):
        self._pool = connection_pool

    async def get_contact_by_email(self, email: EmailStr) -> int | None:
        async with self._pool.connection() as con:
            async with con.cursor() as cur:
                await cur.execute(
                    """
                    SELECT id 
                    FROM demo.contacts
                    WHERE email = %s
                    """, [email]
                )
                res = await cur.fetchone()
                return res[0] if res else res

    async def store_contact(self, contact: Contact) -> int:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO demo.contacts(
                        first_name,
                        last_name,
                        email,
                        user_type
                    )    
                    VALUES (
                        %(first_name)s,
                        %(last_name)s,
                        %(email)s,
                        %(user_type)s
                    )
                    ON CONFLICT DO NOTHING
                    RETURNING ID 
                    """, contact.model_dump()
                )
                res = await cur.fetchone()
                return res[0]

    async def store_student(self, contact_id: int, curriculum: str, enrollment_year: int) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO demo.students(
                        id,
                        curriculum,
                        enrollment_year
                    )
                    VALUES (%s, %s, %s)
                    """, [contact_id, curriculum, enrollment_year]
                )

    async def store_teacher(self, contact_id: int, subject: str) -> None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO demo.teachers(id, subject)
                    VALUES (%s, %s)
                    """, [contact_id, subject]
                )

    async def get_user_type_by_email(self, email: str) -> UserType:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT user_type FROM demo.contacts
                    WHERE email = %s
                    """, [email]
                )
                res = await cur.fetchone()
                return UserType(res[0])
