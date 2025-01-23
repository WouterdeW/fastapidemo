# FastAPI demo project

This is an API that acts as the backend for an online course creation and registration application. It is written in Python and makes use of the FastAPI framework. 
It is not meant to be used in production, but as a demo project. I have tried to play around with as many of the functionalities leveraged by FastAPI, 
without the project becoming too complex. 

## Usecase
This API can be used for six things:

- Create a teacher.
- Create a student.
- Create a course (as a teacher).
- List all courses registered.
- Sign up to a course (both as a teacher or student).
- List all courses the user has signed up to. 

## Architecture
As mentioned, the API makes use of the FastAPI framework. We used a PostgreSQL database to store the data.


## Next steps
- Authentication.
- Use SQLAlchemy.
- Add a date filter on the list all courses endpoint.
- Delete a course registration.
- Ensure only a teacher account can be created with a teacher email.
- Keep track of finished courses.
- etc.