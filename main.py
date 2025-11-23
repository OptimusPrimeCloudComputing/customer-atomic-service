from __future__ import annotations

import os
import socket
from datetime import datetime, UTC
from typing import Dict

from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from models.customer import CustomerRead, CustomerCreate, CustomerUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

customers: Dict[str, CustomerRead] = {}

app = FastAPI(
    title="Customer API",
    description="Atomic Service for managing customer data",
    version="0.0.1",
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

@app.get("/health", response_model=Health)
def get_health():
    return make_health()

@app.post("/customers", response_model=CustomerRead, status_code=201)
def create_customer(customer: CustomerCreate):
    now = datetime.now(UTC)
    uni_id = customer.university_id

    if uni_id in customers:
        raise HTTPException(
            status_code=409,
            detail=f"Customer with university id '{uni_id}' already exists.",
        )

    customer_obj = CustomerRead(
        created_at=now,
        updated_at=now,
        **customer.model_dump(),
    )

    customers[uni_id] = customer_obj
    return customer_obj

@app.get("/customers/{university_id}", response_model=CustomerRead)
def get_customer_by_id(university_id: str):
    customer = customers.get(university_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.patch("/customers/{university_id}", response_model=CustomerRead)
def update_customer(university_id: str, update: CustomerUpdate):
    existing = customers.get(university_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = update.model_dump(exclude_unset=True)
    update_data.pop("university_id", None)

    updated = existing.copy(update=update_data)
    updated.updated_at = datetime.now(UTC)

    customers[university_id] = updated
    return updated

@app.delete("/customers/{university_id}", status_code=204)
def delete_customer(university_id: str):
    if university_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")

    del customers[university_id]
    return JSONResponse(status_code=204, content=None)

@app.get("/")
def root():
    return {
        "message": "Customer Atomic Service (keyed by university_id) use /docs for API documentation.",
        ""
        "endpoints": [
            "/health",
            "/customers",
            "/customers/{university_id}",
        ],
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)