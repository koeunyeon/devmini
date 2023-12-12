from pydantic import BaseModel
from pydantic import EmailStr
from fastapi import Body
from enum import Enum

class MemberRegistSchema(BaseModel):
    email: EmailStr = Body(description="email")

class RegistResultEnum(Enum):
    MEMBER_CREATED = "MEMBER_CREATED"
    MEMBER_CREATE_FAIL = "MEMBER_CREATE_FAIL"
    ACTIVATED_MEMBER = "ACTIVATED_MEMBER"
    EMAIL_KEY_REGEN = "EMAIL_KEY_REGEN"
    EMAIL_KEY_NOT_EXPIRED = "EMAIL_KEY_NOT_EXPIRED"