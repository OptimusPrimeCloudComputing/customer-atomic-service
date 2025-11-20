from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated

# Email must end with .edu
EduEmail = Annotated[str, StringConstraints(pattern=r"^[\w\.-]+@[\w\.-]+\.edu$", strip_whitespace=True)]
CourseIDType = Annotated[str, StringConstraints(pattern=r"^[A-Z]{2,4}\d{3,4}$")]

class CustomerBase(BaseModel):
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Rahul"},
    )
    middle_name: Optional[str] = Field(
        None,
        description="Middle name.",
        json_schema_extra={"example": "Kumar"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Singh"},
    )

    university_id: CourseIDType = Field(
        ...,
        description="University ID (primary identifier in this service).",
        json_schema_extra={"example": "UNI1234"},
    )

    email: EduEmail = Field(
        ...,
        description="Must be a valid .edu email address.",
        json_schema_extra={"example": "rahul@columbia.edu"},
    )

    phone: Optional[str] = Field(
        None,
        description="Contact phone number.",
        json_schema_extra={"example": "+1-646-895-5796"},
    )

    birth_date: Optional[date] = Field(
        None,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example": "2000-07-15"},
    )

    status: str = Field(
        default="active",
        description="Customer status (active, inactive, pending).",
        json_schema_extra={"example": "active"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Rahul",
                "middle_name": "Kumar",
                "last_name": "Singh",
                "university_id": "UNI1234",
                "email": "rahul@columbia.edu",
                "phone": "+1-646-895-5796",
                "birth_date": "2000-07-15",
                "status": "active",
            }
        }
    }


class CustomerCreate(CustomerBase):
    """Creation payload for a Customer (atomic service)."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Rahul",
                    "middle_name": "Kumar",
                    "last_name": "Singh",
                    "university_id": "UNI1234",
                    "email": "rahul@columbia.edu",
                    "phone": "+1-646-895-5796",
                    "birth_date": "2000-07-15",
                    "status": "active",
                }
            ]
        }
    }

class CustomerUpdate(BaseModel):

    first_name: Optional[str] = Field(
        None,
        description="Given name.",
        json_schema_extra={"example": "Rahul"},
    )
    middle_name: Optional[str] = Field(
        None,
        description="Middle name.",
        json_schema_extra={"example": "Kumar"},
    )
    last_name: Optional[str] = Field(
        None,
        description="Family name.",
        json_schema_extra={"example": "Singh"},
    )
    # Intentionally no university_id here (or you could allow but ignore changes)
    email: Optional[EduEmail] = Field(
        None,
        description=".edu email.",
        json_schema_extra={"example": "rahul@columbia.edu"},
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone.",
        json_schema_extra={"example": "+1-646-895-5796"},
    )
    birth_date: Optional[date] = Field(
        None,
        description="DOB (YYYY-MM-DD).",
        json_schema_extra={"example": "2000-07-15"},
    )
    status: Optional[str] = Field(
        None,
        description="Customer status.",
        json_schema_extra={"example": "inactive"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Rahul",
                "middle_name": "K.",
                "last_name": "Singh",
                "email": "rahul@columbia.edu",
                "status": "inactive",
            }
        }
    }


class CustomerRead(CustomerBase):

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
                    "first_name": "Rahul",
                    "middle_name": "Kumar",
                    "last_name": "Singh",
                    "university_id": "UNI0001",
                    "email": "rahul@columbia.edu",
                    "phone": "+1-646-895-5796",
                    "birth_date": "2000-07-15",
                    "status": "active",
                    "created_at": "2025-09-30T10:20:30Z",
                    "updated_at": "2025-09-30T12:00:00Z",
                }
            ]
        }
    }