from typing import Annotated

from fastapi import Depends
from pydantic import EmailStr

from fastapidemo.repositories.contact_repository import ContactRepository


class BaseService:
    def __init__(self, contact_repository: Annotated[ContactRepository, Depends()]):
        self.contact_repo = contact_repository

    async def _validate_email_exists(self, email: EmailStr) -> bool:
        return True if await self.contact_repo.get_contact_by_email(email) else False
