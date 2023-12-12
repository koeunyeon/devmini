from pydantic import BaseModel, Field
from pydantic import EmailStr
from fastapi import Body
from enum import Enum

class MemberRegistRequest(BaseModel):
    email: EmailStr = Body(description="email")

class MemberRegistResponse(str, Enum):
    MEMBER_CREATED = "MEMBER_CREATED"
    MEMBER_CREATE_FAIL = "MEMBER_CREATE_FAIL"
    ACTIVATED_MEMBER = "ACTIVATED_MEMBER"
    EMAIL_KEY_REGEN = "EMAIL_KEY_REGEN"
    EMAIL_KEY_NOT_EXPIRED = "EMAIL_KEY_NOT_EXPIRED"
    WITHDRAW_MEMBER = "WITHDRAW_MEMBER"

class MemberConfirmResponse(str, Enum):
    MEMBER_IS_NOT_EXIST = "MEMBER_IS_NOT_EXIST"
    ACTIVATED_MEMBER_CANT_CONFIRM = "ACTIVATED_MEMBER_CANT_CONFIRM"
    EMAIL_KEY_EXPIRED = "EMAIL_KEY_EXPIRED"
    ACTIVATE_SUCCESS = "ACTIVATE_SUCCESS"

class MemberLoginInputRequest(BaseModel):
    email: EmailStr = Body(description="email")

class MemberLoginInputResponse(str, Enum):
    MEMBER_IS_NOT_EXIST = "MEMBER_IS_NOT_EXIST"
    MEMBER_IS_NOT_ACTIVATE = "MEMBER_IS_NOT_ACTIVATE"
    LOGIN_EMAIL_SEND_SUCCESS = "LOGIN_EMAIL_SEND_SUCCESS"
