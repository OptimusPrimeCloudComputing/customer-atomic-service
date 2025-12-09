from datetime import date

from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from db import Base
from models.customer import CustomerCreate, CustomerRead, CustomerUpdate


class CustomerNotFound(Exception):
    pass


class CustomerAlreadyExists(Exception):
    pass


class Customer(Base):
    __tablename__ = "customers"

    # Use university_id as the primary key
    university_id = Column(String(32), primary_key=True, nullable=False)

    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)

    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(50))

    birth_date = Column(Date)
    status = Column(String(20), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def _to_read_model(self, c: Customer) -> CustomerRead:
        return CustomerRead(
            first_name=c.first_name,
            middle_name=c.middle_name,
            last_name=c.last_name,
            university_id=c.university_id,
            email=c.email,
            phone=c.phone,
            birth_date=c.birth_date,
            status=c.status,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )

    def create(self, customer_in: CustomerCreate) -> CustomerRead:
        existing = (
            self.db.query(Customer)
            .filter(Customer.university_id == customer_in.university_id)
            .first()
        )
        if existing:
            raise CustomerAlreadyExists(
                f"Customer with university id '{customer_in.university_id}' already exists."
            )

        db_customer = Customer(
            university_id=customer_in.university_id,
            first_name=customer_in.first_name,
            middle_name=customer_in.middle_name,
            last_name=customer_in.last_name,
            email=customer_in.email,
            phone=customer_in.phone,
            birth_date=customer_in.birth_date,
            status=customer_in.status,
        )
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)

        return self._to_read_model(db_customer)

    def get_by_university_id(self, university_id: str) -> CustomerRead:
        db_customer = (
            self.db.query(Customer)
            .filter(Customer.university_id == university_id)
            .first()
        )
        if db_customer is None:
            raise CustomerNotFound("Customer not found")

        return self._to_read_model(db_customer)

    def get_by_email(self, email: str) -> CustomerRead:
        db_customer = (
            self.db.query(Customer)
            .filter(Customer.email == email)
            .first()
        )
        if db_customer is None:
            raise CustomerNotFound("Customer not found")

        return self._to_read_model(db_customer)

    def update(self, university_id: str, update_in: CustomerUpdate) -> CustomerRead:
        db_customer = (
            self.db.query(Customer)
            .filter(Customer.university_id == university_id)
            .first()
        )
        if db_customer is None:
            raise CustomerNotFound("Customer not found")

        data = update_in.model_dump(exclude_unset=True)
        data.pop("university_id", None)

        for field, value in data.items():
            setattr(db_customer, field, value)

        self.db.commit()
        self.db.refresh(db_customer)

        return self._to_read_model(db_customer)

    def delete(self, university_id: str) -> None:
        db_customer = (
            self.db.query(Customer)
            .filter(Customer.university_id == university_id)
            .first()
        )
        if db_customer is None:
            raise CustomerNotFound("Customer not found")

        self.db.delete(db_customer)
        self.db.commit()
