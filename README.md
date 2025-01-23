# FastAPI demo project

This is an API that acts as the backend for an online course creation and registration application. It is written in Python and makes use of the FastAPI framework. 
It is not meant to be used in production, but as a demo project. I have tried to play around with as many of the functionalities leveraged by FastAPI, 
without the project becoming too complex. 

## Usecase
This API can currently be used for six things:

- Create a teacher.
- Create a student.
- Create a course (as a teacher).
- List all courses registered.
- Sign up to a course (both as a teacher or student).
- List all courses the user has signed up to. 

The idea is that this backend can be used to create both a student and a teacher account. Only a teacher can then create courses.
Both students and teacher can register to courses (teacher still want to learn ofcourse). There is an option to list all the courses registered and an option to list the 
courses registered per user. The identifier for users is the email address. 

## Deploy
To run this application, including a PostgreSQL database, you need to have Docker installed on your device. Then run in the root of the project
```shell
make build
```
This will build the docker image needed to deploy the app. When finished, you can launch the application with 
```shell
make
```
This deploys two containers. One with the API and one with the database. The `make` command will also deploy all the required objects in the database.
You can now play around with your API via `http://0.0.0.0:80` and get to the documentation via `http://0.0.0.0:80`

## Next steps
- Authentication.
- Use SQLAlchemy.
- Add a date filter on the list all courses endpoint.
- Delete a course registration.
- Ensure only a teacher account can be created with a teacher email.
- Keep track of finished courses.
- etc.