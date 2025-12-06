from __future__ import annotations

import os
import socket
from datetime import datetime, UTC

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from customer_repository import (
    CustomerRepository,
    CustomerNotFound,
    CustomerAlreadyExists,
)
from db import get_db, Base, engine, ensure_database_exists, ensure_tables_exist
from models.customer import CustomerRead, CustomerCreate, CustomerUpdate
from models.health import Health
from sqlalchemy.exc import OperationalError

port = int(os.environ.get("FASTAPIPORT", 8000))

app = FastAPI(
    title="Customer API",
    description="Atomic Service for managing customer data (MySQL-backed, repository pattern)",
    version="0.0.2",
)

# ------------------------------
# Customer Management endpoints
# ------------------------------

def make_health() -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.now(UTC).isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname())
    )

# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    try:
        # Step 1: Ensure database exists
        ensure_database_exists()

        # Step 2: Ensure custom tables exist (like addresses)
        ensure_tables_exist()

        # Step 3: Create tables from SQLAlchemy models
        Base.metadata.create_all(bind=engine)

        print("DB connected & all tables ensured at startup.")
    except OperationalError as e:
        print(f"DB initialization FAILED at startup: {e}")
    except Exception as e:
        print(f"Startup error: {e}")

@app.get("/health", response_model=Health)
def get_health():
    return make_health()

@app.post("/customers", response_model=CustomerRead, status_code=201)
def create_customer(
        customer: CustomerCreate,
        db: Session = Depends(get_db),
):
    repo = CustomerRepository(db)
    try:
        return repo.create(customer)
    except CustomerAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/customers/{university_id}", response_model=CustomerRead)
def get_customer_by_id(
    university_id: str,
    db: Session = Depends(get_db),
):
    repo = CustomerRepository(db)
    try:
        return repo.get_by_university_id(university_id)
    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.patch("/customers/{university_id}", response_model=CustomerRead)
def update_customer(
    university_id: str,
    update: CustomerUpdate,
    db: Session = Depends(get_db),
):
    repo = CustomerRepository(db)
    try:
        return repo.update(university_id, update)
    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/customers/{university_id}", status_code=204)
def delete_customer(
    university_id: str,
    db: Session = Depends(get_db),
):
    repo = CustomerRepository(db)
    try:
        repo.delete(university_id)
    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return JSONResponse(status_code=204, content=None)

@app.get("/")
def root():
    return {
        "message": "Customer Atomic Service (keyed by university_id) use /docs for API documentation.",
        "endpoints": [
            "/health",
            "/customers",
            "/customers/{university_id}",
        ],
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)