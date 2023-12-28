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
    email: EmailStr = Field(description="email")

class MemberLoginInputResponse(str, Enum):
    MEMBER_IS_NOT_EXIST = "MEMBER_IS_NOT_EXIST"
    MEMBER_IS_NOT_ACTIVATE = "MEMBER_IS_NOT_ACTIVATE"
    LOGIN_EMAIL_SEND_SUCCESS = "LOGIN_EMAIL_SEND_SUCCESS"


# 클래스 기반은 안되네. 그러면 필드 기반으로 해 볼까.

email: EmailStr = Field(description="email")
# to Query, Path ... Query 가 문제인데. path는 함수 기반으로 인지하고, body는 기본값인데. Query는 어쩌지.

# 일단 이건 작동은 함. 미리 필드들을 정의해 두고, 동적으로 클래스를 만들면.. 장점이 있나?

class Sample(BaseModel):
    email: EmailStr = email