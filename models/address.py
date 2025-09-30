from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    street: str = Field(
        ...,
        description="Street address",
        json_schema_extra={"example": "123 Broadway Ave"},
    )
    city: str = Field(
        ...,
        description="City name.",
        json_schema_extra={"example": "New York"},
    )
    state: str = Field(
        ...,
        description="State or region.",
        json_schema_extra={"example": "NY"},
    )
    postal_code: str = Field(
        ...,
        description="ZIP or postal code.",
        json_schema_extra={"example": "10001"},
    )
    country: str = Field(
        ...,
        description="Country name.",
        json_schema_extra={"example": "USA"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "street": "123 Broadway Ave",
                "city": "New York",
                "state": "NY",
                "postal_code": "10027",
                "country": "USA",
            }
        }
    }


class AddressCreate(AddressBase):
    """Payload for creating a new address."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "street": "123 Broadway Ave",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10027",
                    "country": "USA",
                }
            ]
        }
    }


class AddressUpdate(BaseModel):
    """Partial update for an Address; supply only fields to change."""
    street: Optional[str] = Field(None, description="Street address", json_schema_extra={"example": "456 Elm St"})
    city: Optional[str] = Field(None, description="City name", json_schema_extra={"example": "Boston"})
    state: Optional[str] = Field(None, description="State or region", json_schema_extra={"example": "MA"})
    postal_code: Optional[str] = Field(None, description="ZIP or postal code", json_schema_extra={"example": "02118"})
    country: Optional[str] = Field(None, description="Country name", json_schema_extra={"example": "USA"})

    model_config = {
        "json_schema_extra": {
            "example": {
                "city": "Boston",
                "state": "MA"
            }
        }
    }


class AddressRead(AddressBase):
    """Server representation returned to clients."""
    address_id: UUID = Field(
        default_factory=uuid4,
        description="System-generated unique Address ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-09-30T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-09-30T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "address_id": "99999999-9999-4999-8999-999999999999",
                    "street": "123 Broadway Ave",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10027",
                    "country": "USA",
                    "created_at": "2025-09-30T10:20:30Z",
                    "updated_at": "2025-09-30T12:00:00Z",
                }
            ]
        }
    }