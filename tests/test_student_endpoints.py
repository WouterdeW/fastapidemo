import pytest

from fastapidemo.models import Student


class TestsStudent:

    @pytest.mark.asyncio
    async def test_create_student(self, test_client):
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            curriculum="Quantum mechanics",
            enrollment_year="2023"
        )

        res = await test_client.put("/users/create/student", json=student.model_dump())
        assert res.status_code == 201
        assert "Successfully" in res.text

    @pytest.mark.asyncio
    async def test_create_student_email_exists(self, test_client):
        student = Student(
            first_name="John",
            last_name="Doe",
            email="john@dot.com",
            curriculum="Quantum mechanics",
            enrollment_year="2023"
        )
        second_student = Student(
            first_name="John",
            last_name="Doeter",
            email="john@dot.com",
            curriculum="Quantum mechanics",
            enrollment_year="2023"
        )
        first_res = await test_client.put("/users/create/student", json=student.model_dump())
        second_res = await test_client.put("/users/create/student", json=second_student.model_dump())
        assert first_res.status_code == 201
        assert second_res.status_code == 400

    @pytest.mark.asyncio
    async def test_create_student_with_faulty_email(self, test_client):
        student = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndot.com",
            "curriculum": "Quantum mechanics",
            "enrollment_year": "2023"
        }

        res = await test_client.put("/users/create/student", json=student)
        assert res.status_code == 422
