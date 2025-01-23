from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import EmailStr

from fastapidemo.models import Course, UserType
from fastapidemo.repositories.base_service import BaseService
from fastapidemo.repositories.contact_repository import ContactRepository
from fastapidemo.repositories.course_repository import CourseRepository


class CourseService(BaseService):
    def __init__(
            self,
            contact_repository: Annotated[ContactRepository, Depends()],
            course_repository: Annotated[CourseRepository, Depends()]
    ):
        super().__init__(contact_repository)
        self.course_repo = course_repository

    async def _validate_user_type(self, email: str) -> bool:
        user_type = await self.contact_repo.get_user_type_by_email(email)
        return True if user_type == UserType.teacher else False

    async def create_new_course(self, course: Course, email: str) -> int:
        if not await self._validate_user_type(email):
            raise HTTPException(status_code=400, detail="Only teachers can register a new course.")

        return await self.course_repo.store_course(course)

    async def register_user_to_course(self, course: Course, email: EmailStr) -> int | None:
        if not (contact_id := await self.contact_repo.get_contact_by_email(email)):
            raise HTTPException(status_code=400, detail="No account for this email.")

        if not (course_id := await self.course_repo.get_course_id_by_name(course.name)):
            raise HTTPException(status_code=400, detail="No Course exists with this name.")

        if not (registration_id := await self.course_repo.store_course_registration(course_id, contact_id)):
            raise HTTPException(status_code=400, detail="A registration already exists for this Course and account.")

        return registration_id

    async def list_all_courses(self) -> list[Course] | None:
        return await self.course_repo.get_all_courses()

    async def list_all_courses_for_contact(self, email: EmailStr) -> list[Course] | None:
        if not await self._validate_email_exists(email):
            raise HTTPException(status_code=400, detail="No account for this email.")

        return await self.course_repo.get_registered_courses_by_email(email)
