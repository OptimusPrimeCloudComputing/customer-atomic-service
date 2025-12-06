# In db.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = os.getenv("DB_USER", "root")
# DB_PASS = os.getenv("DB_PASS", "TestPass123@")
DB_PASS = ('TestPass@123')
DB_NAME = os.getenv("DB_NAME", "customer")
DB_HOST = os.getenv("DB_HOST", "34.171.164.80")
DB_PORT = os.getenv("DB_PORT", "3306")

def ensure_database_exists():
    """Create database if it doesn't exist using SQL with charset/collation"""
    # Connect without specifying a database
    temp_url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/"
    temp_engine = create_engine(temp_url)

    try:
        with temp_engine.connect() as conn:
            # Create database if not exists
            conn.execute(text(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                f"CHARACTER SET utf8mb4 "
                f"COLLATE utf8mb4_unicode_ci"
            ))
            conn.commit()
            print(f"Database '{DB_NAME}' ensured to exist with utf8mb4.")
    except Exception as e:
        print(f"Error ensuring database exists: {e}")
        raise
    finally:
        temp_engine.dispose()

def ensure_tables_exist():
    """Create addresses table if it doesn't exist"""
    try:
        with engine.connect() as conn:
            # Create addresses table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS addresses (
                  address_id    CHAR(36)      NOT NULL,
                  university_id VARCHAR(32)   NOT NULL,
                  street        VARCHAR(255)  NOT NULL,
                  city          VARCHAR(100)  NOT NULL,
                  state         VARCHAR(50)   NOT NULL,
                  postal_code   VARCHAR(20)   NOT NULL,
                  country       VARCHAR(100)  NOT NULL,
                  created_at    DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
                  updated_at    DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                                               ON UPDATE CURRENT_TIMESTAMP(6),
                  PRIMARY KEY (address_id),
                  KEY idx_addresses_university_id (university_id)
                )
            """))
            conn.commit()
            print("Table 'addresses' ensured to exist.")
    except Exception as e:
        print(f"Error ensuring tables exist: {e}")
        raise

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()