import ast

import pytest

from fastapidemo.models import Student


class TestsCourses:

    @pytest.mark.asyncio
    async def test_register_to_and_get_course(self, test_client, create_course):
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            curriculum="Quantum mechanics",
            enrollment_year="2023"
        )
        course = {"name": "Intro to quantum mechanics", "subject": "Physics", "start_date": "2025-02-01"}
        body = {"course": course, "email": student.email}
        await test_client.put("/users/create/student", json=student.model_dump())
        await test_client.put("/courses/register", json=body)
        third_res = await test_client.get("/courses/get/user", params={"email": student.email})
        course_list = ast.literal_eval(third_res.text)
        assert len(course_list) == 1
        assert course_list[0] == course

    @pytest.mark.asyncio
    async def test_register_to_course_not_exits(self, test_client):
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            curriculum="Quantum mechanics",
            enrollment_year="2023"
        )
        course = {"name": "Intro to quantum mechanics", "subject": "Physics", "start_date": "2025-02-01"}
        body = {"course": course, "email": student.email}
        await test_client.put("/users/create/student", json=student.model_dump())
        res = await test_client.put("/courses/register", json=body)
        assert res.status_code == 400

    @pytest.mark.asyncio
    async def test_register_with_no_account(self, test_client):
        email = "not@registered.com"
        course = {"name": "Intro to quantum mechanics", "subject": "Physics", "start_date": "2025-02-01"}
        body = {"course": course, "email": email}
        res = await test_client.put("/courses/register", json=body)
        assert res.status_code == 400

    @pytest.mark.asyncio
    async def test_double_registration(self, test_client):
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            curriculum="Quantum mechanics",
            enrollment_year="2023"
        )
        course = {"name": "Intro to quantum mechanics", "subject": "Physics", "start_date": "2025-02-01"}
        body = {"course": course, "email": student.email}
        await test_client.put("/users/create/student", json=student.model_dump())
        await test_client.put("/courses/register", json=body)
        res = await test_client.put("/courses/register", json=body)
        assert res.status_code == 400
