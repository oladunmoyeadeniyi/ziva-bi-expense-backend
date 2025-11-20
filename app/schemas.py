from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExpenseCreate(BaseModel):
    employee_name: str
    employee_id: str
    amount: float
    currency: Optional[str] = 'NGN'
    category: Optional[str] = 'General'

class ExpenseOut(BaseModel):
    id: str
    employee_name: str
    employee_id: str
    status: str
    amount: float
    currency: str
    category: Optional[str]
    created_at: datetime
    file_path: str
    approver_comment: Optional[str] = None

    class Config:
        orm_mode = True
