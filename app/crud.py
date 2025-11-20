from sqlalchemy.orm import Session
from . import models, schemas

def create_expense(db: Session, *, filename: str, expense_in: schemas.ExpenseCreate):
    exp = models.Expense(
        employee_name=expense_in.employee_name,
        employee_id=expense_in.employee_id,
        amount=expense_in.amount,
        currency=expense_in.currency,
        category=expense_in.category,
        file_path=filename,
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

def list_expenses(db: Session, limit: int = 100):
    return db.query(models.Expense).order_by(models.Expense.created_at.desc()).limit(limit).all()

def get_expense(db: Session, expense_id: str):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def set_status(db: Session, expense_id: str, status: str, comment: str = None):
    exp = get_expense(db, expense_id)
    if not exp:
        return None
    exp.status = status
    exp.approver_comment = comment
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp
