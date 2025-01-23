from fastapi import FastAPI

from .router import contact_router, course_router

app = FastAPI()
app.include_router(contact_router)
app.include_router(course_router)
