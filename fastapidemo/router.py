from typing import Annotated

from fastapi import APIRouter, Depends, Body
from pydantic import EmailStr

from .models import Student, Teacher, Course
from .services.contact_service import ContactService
from .services.course_service import CourseService

contact_router = APIRouter(prefix="/users")
course_router = APIRouter(prefix="/courses")


@contact_router.put("/create/student", status_code=201)
async def create_student(student: Student, contact_service: Annotated[ContactService, Depends()]) -> str:
    student_id = await contact_service.create_student(student)
    return f"Successfully created student account with ID {student_id}."


@contact_router.put("/create/teacher", status_code=201)
async def create_teacher(teacher: Teacher, contact_service: Annotated[ContactService, Depends()]) -> str:
    teacher_id = await contact_service.create_teacher(teacher)
    return f"Successfully created teacher account with ID {teacher_id}."


@course_router.get("/get/user")
async def get_registered_courses(email: EmailStr, course_service: Annotated[CourseService, Depends()]) -> list[Course] | None:
    return await course_service.list_all_courses_for_contact(email)


@course_router.put("/create", status_code=201)
async def create_course(course: Course, email: Annotated[EmailStr, Body()], course_service: Annotated[CourseService, Depends()]) -> str:
    course_id = await course_service.create_new_course(course, email)
    return f"Successfully created course with ID {course_id}."


@course_router.put("/register", status_code=201)
async def register_to_course(course: Course, email: Annotated[EmailStr, Body()], course_service: Annotated[CourseService, Depends()]) -> str:
    course_id = await course_service.register_user_to_course(course, email)

    return f"Successfully created new course with ID {course_id}."


@course_router.get("/all")
async def get_all_available_courses(course_service: Annotated[CourseService, Depends()]) -> list[Course]:
    return await course_service.list_all_courses()
