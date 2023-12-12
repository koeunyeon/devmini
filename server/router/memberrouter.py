from fastapi import APIRouter, Path
from schema import memberschema
from service import memberservice
from keyfa.util import rdbutil, dateutil
from config import Config

router = APIRouter(prefix="/member", tags=["member"])

@router.post("/regist")
async def regist(email_schema: memberschema.MemberRegistRequest) -> memberschema.MemberRegistResponse:
    member = await rdbutil.first("member", email=email_schema.email)    
    if member is None:
        email_key = await memberservice.generate_email_key()
        expired_at = await memberservice.get_expired_at()
        pk = await rdbutil.insert("member", 
            email=email_schema.email,
            email_key=email_key,
            expired_at=expired_at
        )
        if pk is not None:
            return memberschema.MemberRegistResponse.MEMBER_CREATED
        else:
            return memberschema.MemberRegistResponse.MEMBER_CREATE_FAIL
    elif member.status == "EMAIL_NOT_CONFIRMED": # 이메일 확인 안됨.
        if dateutil.is_not_over(member.expired_at): # 이메일 인증키 살아있음.
            return memberschema.MemberRegistResponse.EMAIL_KEY_NOT_EXPIRED
        else:
            email_key = await memberservice.generate_email_key()
            expired_at = await memberservice.get_expired_at()
            
            await rdbutil.update(
                target_table="member",
                terms=dict(
                    id = member.id
                ),
                values=dict(
                    email_key = email_key, 
                    expired_at = expired_at
                )
            )
            return memberschema.MemberRegistResponse.EMAIL_KEY_REGEN
    elif member.status == "ACTIVATED":
        return memberschema.MemberRegistResponse.ACTIVATED_MEMBER
    elif member.status == "WITHDRAW":
        return memberschema.MemberRegistResponse.WITHDRAW_MEMBER

@router.get("/confirm/{email_key}")
async def confirm(email_key: str = Path(description="email key")) -> memberschema.MemberConfirmResponse:
    member = await rdbutil.first("member", email_key=email_key)
    if member is None:
        return memberschema.MemberConfirmResponse.MEMBER_IS_NOT_EXIST
    
    if member.status != "EMAIL_NOT_CONFIRMED":
        return memberschema.MemberConfirmResponse.ACTIVATED_MEMBER_CANT_CONFIRM
    
    if dateutil.is_over(member.expired_at):
        return memberschema.MemberConfirmResponse.EMAIL_KEY_EXPIRED    
        
    await rdbutil.update(
            "member",
            terms=dict(
                id = member.id
            ),
            values=dict(
                status = "ACTIVATED"
            )
        )
    return memberschema.MemberConfirmResponse.ACTIVATE_SUCCESS
    
