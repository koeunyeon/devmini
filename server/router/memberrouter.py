from fastapi import APIRouter
from schema.memberschema import MemberRegistSchema
from service import memberservice

router = APIRouter(prefix="/regist", tags=["member"])

@router.post("/regist")
async def regist(email_schema: MemberRegistSchema) -> memberservice.RegistResultEnum:
    member_regist_result = await memberservice.regist(email_schema.email)
    return member_regist_result