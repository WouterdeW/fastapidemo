import pytest

from fastapidemo.models import Teacher, Student


class TestsTeachers:

    @pytest.mark.asyncio
    async def test_create_teacher(self, test_client):
        teacher = Teacher(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            subject="Physics"
        )

        res = await test_client.put("/users/create/teacher", json=teacher.model_dump())
        assert res.status_code == 201
        assert "Successfully" in res.text

    @pytest.mark.asyncio
    async def test_create_teacher_email_exists(self, test_client):
        teacher = Teacher(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            subject="Physics"
        )
        second_teacher = Teacher(
            first_name="John",
            last_name="Doeter",
            email="john@dot.com",
            subject="Physics"
        )
        first_res = await test_client.put("/users/create/teacher", json=teacher.model_dump())
        second_res = await test_client.put("/users/create/teacher", json=second_teacher.model_dump())
        assert first_res.status_code == 201
        assert second_res.status_code == 400

    @pytest.mark.asyncio
    async def test_create_course(self, test_client):
        teacher = Teacher(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            subject="Physics"
        )
        await test_client.put("/users/create/teacher", json=teacher.model_dump())

        course = {"name": "Intro to quantum mechanics", "subject": "Physics", "start_date": "2025-02-01"}
        body = {"course": course, "email": teacher.email}

        res = await test_client.put("/courses/create", json=body)
        assert res.status_code == 201

    @pytest.mark.asyncio
    async def test_create_course(self, test_client):
        teacher = Teacher(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            subject="Physics"
        )
        await test_client.put("/users/create/teacher", json=teacher.model_dump())

        course = {"name": "Intro to quantum mechanics", "subject": "Physics", "start_date": "2025-02-01"}
        body = {"course": course, "email": teacher.email}

        res = await test_client.put("/courses/create", json=body)
        assert res.status_code == 201

    @pytest.mark.asyncio
    async def test_create_course_with_student_account(self, test_client):
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            curriculum="Quantum mechanics",
            enrollment_year="2023"
        )

        await test_client.put("/users/create/student", json=student.model_dump())
        course = {"name": "Intro to quantum mechanics", "subject": "Physics", "start_date": "2025-02-01"}
        body = {"course": course, "email": student.email}

        res = await test_client.put("/courses/create", json=body)
        assert res.status_code == 400
