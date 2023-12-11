from pydantic import BaseModel
from pydantic import EmailStr
from fastapi import Body

class MemberRegistSchema(BaseModel):
    email: EmailStr = Body(description="email")
