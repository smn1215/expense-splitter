import sqlite3
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Expense Splitter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payer TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class ExpenseCreate(BaseModel):
    payer: str
    amount: float
    description: str

@app.get("/api/expenses")
def get_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, payer, amount, description FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    
    expenses = [{"id": r[0], "payer": r[1], "amount": r[2], "description": r[3]} for r in rows]
    total_spent = sum(e["amount"] for e in expenses)
    
    return {"expenses": expenses, "total_spent": total_spent}

@app.post("/api/expenses", status_code=201)
def add_expense(expense: ExpenseCreate):
    if expense.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (payer, amount, description) VALUES (?, ?, ?)",
        (expense.payer, expense.amount, expense.description)
    )
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()
    
    return {"id": expense_id, **expense.dict()}
