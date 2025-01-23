from fastapi import HTTPException

from fastapidemo.models import Student, Teacher
from fastapidemo.repositories.base_service import BaseService


class ContactService(BaseService):

    async def create_student(self, student: Student) -> int:
        if not await self._validate_email_exists(student.email):
            contact_id = await self.contact_repo.store_contact(student)
            await self.contact_repo.store_student(contact_id, student.curriculum, student.enrollment_year)
            return contact_id
        else:
            raise HTTPException(status_code=400, detail="An account already exists with this email.")

    async def create_teacher(self, teacher: Teacher) -> int:
        if not await self._validate_email_exists(teacher.email):
            contact_id = await self.contact_repo.store_contact(teacher)
            await self.contact_repo.store_teacher(contact_id, teacher.subject)
            return contact_id
        else:
            raise HTTPException(status_code=400, detail="An account already exists with this email.")
