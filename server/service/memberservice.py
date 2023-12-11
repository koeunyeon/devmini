import uuid
from datetime import datetime, timedelta
from enum import Enum
from keyfa.util import rdbutil
from config import Config

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

class RegistResultEnum(Enum):
    MEMBER_CREATED = "MEMBER_CREATED"
    MEMBER_CREATE_FAIL = "MEMBER_CREATE_FAIL"
    ACTIVATED_MEMBER = "ACTIVATED_MEMBER"
    EMAIL_KEY_REGEN = "EMAIL_KEY_REGEN"
    EMAIL_KEY_NOT_EXPIRED = "EMAIL_KEY_NOT_EXPIRED"

async def regist(email) -> RegistResultEnum:
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
        rdbutil.update("member", email_key=email_key, expired_at=expired_at)
        return RegistResultEnum.EMAIL_KEY_REGEN
    else:
        return RegistResultEnum.EMAIL_KEY_NOT_EXPIRED