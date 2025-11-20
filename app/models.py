from sqlalchemy import Column, String, Float, Text, DateTime
from sqlalchemy.sql import func
from .database import Base
import uuid

def generate_id():
    return uuid.uuid4().hex

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(String, primary_key=True, default=generate_id)
    employee_name = Column(String(200), nullable=False)
    employee_id = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default='PENDING')
    amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(10), nullable=False, default='NGN')
    category = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(Text, nullable=False)
    approver_comment = Column(Text, nullable=True)
