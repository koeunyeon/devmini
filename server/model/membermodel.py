from keyfa.model.basemodel import BaseModel
from keyfa.util.modelutil import column_by_rule

class MemberModel(BaseModel):
    email = column_by_rule("email", nullable=False)
    email_key = column_by_rule("email_key")
    expired_at = column_by_rule("expired_at")
    status = column_by_rule("status", default='email_not_confirmed', nullable=False)