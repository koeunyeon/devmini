import uuid
from enum import Enum

from keyfa.util import rdbutil, dateutil
from config import Config

class MemberStatus(str, Enum):
    NOT_EXIST = "NOT_EXIST"
    EMAIL_NOT_CONFIRMED = "EMAIL_NOT_CONFIRMED"
    ACTIVATED = "ACTIVATED"
    WITHDRAW = "WITHDRAW"

    @classmethod
    def get(cls, member):
        if member is None:
            return cls.NOT_EXIST
        return cls[member.status]

async def generate_email_key():
    while True:
        temp_email_key = str(uuid.uuid4())
        if not await rdbutil.exist("member", email_key = temp_email_key):
            return temp_email_key

async def get_expired_at():
    dateutil.add(hours=Config.extra.regist_expired_hour)

async def send_regist_email(email, email_key):
    "todo : implements"
    pass

async def send_login_email(email, email_key):
    "todo : implements"
    pass