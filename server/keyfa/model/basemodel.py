from sqlalchemy import Column, DateTime, Integer, func, CHAR

class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    use_yn = Column(CHAR(1), nullable=False, default='Y')