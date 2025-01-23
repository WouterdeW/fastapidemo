from fastapi import FastAPI

from .router import contact_router, course_router

app = FastAPI()
app.include_router(contact_router)
app.include_router(course_router)


@app.get("/")
def read_root():
    return "Welcome to the FastAPI demo. Please see /docs for more information on the endpoints."
