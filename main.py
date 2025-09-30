from __future__ import annotations

import os
import socket
from datetime import datetime, UTC
from typing import Dict, List
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from starlette.responses import JSONResponse

from models.address import AddressBase, AddressRead, AddressCreate, AddressUpdate
from models.customer import CustomerRead, CustomerCreate, CustomerUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------

app = FastAPI(
    title="Customer API",
    description="Service for managing customer data",
    version="0.0.1",
)

# -----------------------------------------------------------------------------
# Customer Management endpoints
# -----------------------------------------------------------------------------

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
    """
    Dummy implementation: returns a CustomerRead object without saving to a real database.
    """
    return CustomerRead(
        customer_id=uuid4(),
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        **customer.model_dump()
    )

@app.get("/customers/{customer_id}", response_model=CustomerRead)
def get_customer_by_id(customer_id: str):
    return CustomerRead(
        customer_id=uuid4(),
        first_name="Rahul",
        middle_name="K.",
        last_name="Singh",
        university_id="UNI0001",
        email="rahul.singh@columbia.edu",
        phone="+1-555-123-4567",
        birth_date=datetime(1995, 5, 20).date(),
        status="active",
        address=[
            AddressBase(
                street="123 Broadway Ave",
                city="New York",
                state="NY",
                postal_code="10027",
                country="USA",
            )
        ],
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

@app.patch("/courses/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: str, update: CustomerUpdate):
    existing = CustomerRead(
        customer_id=uuid4(),
        first_name="Rahul",
        middle_name="K.",
        last_name="Singh",
        university_id="UNI0001",
        email="rahul.singh@columbia.edu",
        phone="+1-555-123-4567",
        birth_date=datetime(1995, 5, 20).date(),
        status="active",
        address=[
            AddressBase(
                street="123 Broadway Ave",
                city="New York",
                state="NY",
                postal_code="10027",
                country="USA",
            )
        ],
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # Merge updates into the existing record
    data = existing.model_dump()
    data.update(update.model_dump(exclude_unset=True))
    data["updated_at"] = datetime.now(UTC)

    return CustomerRead(**data)

@app.delete("/courses/{customer_id}", status_code=204)
def delete_customer(customer_id: str):
    return JSONResponse(status_code=204, content=None)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------
@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    """
    Dummy implementation: returns an AddressRead with generated ID and timestamps.
    """
    return AddressRead(
        address_id=uuid4(),
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        **address.model_dump()
    )

@app.get("/customers/{customer_id}/addresses", response_model=List[AddressRead])
def list_customer_addresses(customer_id: str):
    """
    Dummy implementation: returns a static list of addresses for the given customer_id.
    """
    # Return a dummy list of addresses
    return [
        AddressRead(
            address_id=uuid4(),
            street="123 Broadway Ave",
            city="New York",
            state="NY",
            postal_code="10027",
            country="USA",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        ),
        AddressRead(
            address_id=uuid4(),
            street="456 Elm Street",
            city="Boston",
            state="MA",
            postal_code="02118",
            country="USA",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        ),
    ]

@app.patch("/customers/{customer_id}/addresses/{address_id}",
           response_model=AddressRead
           )
def update_address(customer_id: str, address_id: str, update: AddressUpdate):
    existing = AddressRead(
        address_id=uuid4(),
        street="123 Broadway Ave",
        city="New York",
        state="NY",
        postal_code="10027",
        country="USA",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    data = existing.model_dump()
    data.update(update.model_dump(exclude_unset=True))
    data["updated_at"] = datetime.now(UTC)

    return AddressRead(**data)

@app.delete("/customers/{customer_id}/addresses/{address_id}", status_code=204)
def delete_address(address_uni: str):
    return

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Columbia's Second hand store API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
