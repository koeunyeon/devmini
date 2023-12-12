import uuid
from keyfa.util import rdbutil, dateutil
from config import Config

async def generate_email_key():
    while True:
        temp_email_key = str(uuid.uuid4())
        if not await rdbutil.exist("member", email_key = temp_email_key):
            return temp_email_key

async def get_expired_at():
    dateutil.add(hours=Config.extra.regist_expired_hour)

async def send_regist_email(email):
    "todo : implements"
    pass 