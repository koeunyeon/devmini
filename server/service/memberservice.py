import uuid
from datetime import datetime, timedelta
from keyfa.util import rdbutil
from config import Config
from schema.memberschema import RegistResultEnum

async def member_exist(email):
    return await rdbutil.exist("member", email=email)

async def generate_email_key():
    while True:
        temp_email_key = str(uuid.uuid4())
        if not await rdbutil.exist("member", email_key = temp_email_key):
            return temp_email_key

async def send_regist_email(email):
    "todo : implements"
    pass

async def regist(email: str) -> RegistResultEnum:
    if not await member_exist(email=email):
        email_key = await generate_email_key()
        expired_at = datetime.now() + timedelta(hours=Config.extra.regist_expired_hour)
        pk = await rdbutil.insert("member", 
            email=email,
            email_key=email_key,
            expired_at=expired_at
        )

        if pk is not None:
            return RegistResultEnum.MEMBER_CREATED
        else:
            return RegistResultEnum.MEMBER_CREATE_FAIL
    
    member = await rdbutil.first("member", email=email)
    if member.status == "activated":
        return RegistResultEnum.ACTIVATED_MEMBER
    
    if datetime.now() > member.expired_at:
        email_key = await generate_email_key()
        expired_at = datetime.now() + timedelta(hours=Config.extra.regist_expired_hour)
        
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
        
        return RegistResultEnum.EMAIL_KEY_REGEN
    else:
        return RegistResultEnum.EMAIL_KEY_NOT_EXPIRED