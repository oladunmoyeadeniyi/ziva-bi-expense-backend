# fastapi main app for Ziva BI Expense Module (demo)
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os, uuid

from . import crud, models, schemas
from .database import engine, get_db
from .config import UPLOAD_DIR

# create tables (safe on startup)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ziva BI - Expense Module (Backend)", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/expenses", response_model=schemas.ExpenseOut, status_code=201)
async def create_expense(
    employee_name: str = Form(...),
    employee_id: str = Form(...),
    amount: float = Form(...),
    currency: str = Form("NGN"),
    category: str = Form("General"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # validate extension
    filename = file.filename
    ext = filename.split('.')[-1].lower()
    if ext not in {"png","jpg","jpeg","pdf"}:
        raise HTTPException(status_code=400, detail="Invalid file type")
    safe_name = f"{uuid.uuid4().hex}_{filename}"
    save_path = os.path.join(UPLOAD_DIR, safe_name)
    # write file content
    with open(save_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    expense = crud.create_expense(db, filename=safe_name, expense_in=schemas.ExpenseCreate(
        employee_name=employee_name,
        employee_id=employee_id,
        amount=amount,
        currency=currency,
        category=category
    ))
    return expense

@app.get("/api/expenses", response_model=list[schemas.ExpenseOut])
def list_expenses(db: Session = Depends(get_db)):
    return crud.list_expenses(db)

@app.post("/api/expenses/{expense_id}/approve", response_model=schemas.ExpenseOut)
def approve(expense_id: str, comment: str = Form("Approved"), db: Session = Depends(get_db)):
    exp = crud.set_status(db, expense_id, "APPROVED", comment)
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    return exp

@app.post("/api/expenses/{expense_id}/reject", response_model=schemas.ExpenseOut)
def reject(expense_id: str, comment: str = Form("Rejected"), db: Session = Depends(get_db)):
    exp = crud.set_status(db, expense_id, "REJECTED", comment)
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    return exp

@app.get('/uploads/{filename}')
def serve_file(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(path)
