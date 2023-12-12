from fastapi import APIRouter, Path
from schema import memberschema
from service import memberservice
from keyfa.util import rdbutil, dateutil


router = APIRouter(prefix="/member", tags=["member"])

@router.post("/regist", description="클라이언트에서 사용자 생성을 위한 이메일 입력")
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

@router.get("/regist/confirm/{email_key}", description="이메일 확인 링크 클릭시 이메일 키 인증.")
async def regist_confirm(email_key: str = Path(description="email key")) -> memberschema.MemberConfirmResponse:
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
    
@router.post("/login", description="로그인을 위한 이메일 입력")
async def login_input(email_schema: memberschema.MemberLoginInputRequest) -> memberschema.MemberLoginInputResponse:
    member = await rdbutil.first("member", email=email_schema.email)    
    member_status = memberservice.MemberStatus.get(member)
    if member_status == memberservice.MemberStatus.NOT_EXIST:
        return memberschema.MemberLoginInputResponse.MEMBER_IS_NOT_EXIST
    if member_status != memberservice.MemberStatus.ACTIVATED:
        return memberschema.MemberLoginInputResponse.MEMBER_IS_NOT_ACTIVATE
    
    memberservice.send_login_email(email_schema.email, member.email_key)
    return memberschema.MemberLoginInputResponse.LOGIN_EMAIL_SEND_SUCCESS

@router.get("/login/confirm/{email_key}", description="이메일 로그인 링크 클릭시 로그인")
async def login_confirm(email_key: str = Path(description="email key")):
    pass

    