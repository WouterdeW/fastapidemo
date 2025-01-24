from psycopg.rows import class_row
from pydantic import EmailStr

from fastapidemo.models import Course
from fastapidemo.repositories.db_connection import ConnectDeps


class CourseRepository:
    def __init__(self, connection_pool: ConnectDeps):
        self._pool = connection_pool

    async def store_course(self, course: Course) -> int:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO demo.courses(name, subject, start_date)
                    VALUES (%(name)s, %(subject)s, %(start_date)s)
                    RETURNING id
                    """, course.model_dump()
                )
                res = await cur.fetchone()
                return res[0]

    async def store_course_registration(self, course_id: int, contact_id: int) -> int:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO demo.course_registrations (course_id, contact_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    RETURNING id
                    """, [course_id, contact_id]
                )
                res = await cur.fetchone()
                return res[0] if res else res

    async def get_course_id_by_name(self, name: str) -> int | None:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT id FROM demo.courses
                    WHERE name = %s
                    """, [name]
                )
                res = await cur.fetchone()
                return res[0] if res else res

    async def get_all_courses(self) -> list[Course] | None:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Course)) as cur:
                await cur.execute(
                    """
                    SELECT name, subject, start_date
                    FROM courses
                    """
                )
                return await cur.fetchall()

    async def get_registered_courses_by_email(self, email: EmailStr) -> list[Course] | None:
        async with self._pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Course)) as cur:
                await cur.execute(
                    """
                    WITH registrations AS (
                        SELECT course_id
                        FROM course_registrations
                        WHERE contact_id IN (
                            SELECT id FROM contacts WHERE email = %s
                        )
                    )
                    SELECT name, subject, start_date
                    FROM registrations r
                    LEFT JOIN courses c 
                    ON c.id = r.course_id
                    """, [email]
                )
                return await cur.fetchall()
