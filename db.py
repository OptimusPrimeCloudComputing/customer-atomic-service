import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# DB_USER = os.getenv("DB_USER", "myapp_user")
# DB_PASS = os.getenv("DB_PASS", "TestPass@123")
# DB_NAME = os.getenv("DB_NAME", "customer")

DB_USER = "myapp_user"
DB_PASS = "TestPass@123"
DB_NAME = "customer"

# Cloud Run uses Unix socket via built-in Cloud SQL connector
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")  # e.g., "project:region:instance"

# Encode password for URL
encoded_pass = quote_plus(DB_PASS)

if INSTANCE_CONNECTION_NAME:
    # ===== CLOUD RUN =====
    # Uses Unix socket - Cloud Run has built-in Cloud SQL proxy
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_pass}@/{DB_NAME}?unix_socket=/cloudsql/{INSTANCE_CONNECTION_NAME}"
    print(f"Using Cloud Run Cloud SQL connection: {INSTANCE_CONNECTION_NAME}")
else:
    # ===== LOCAL DEVELOPMENT =====
    # Uses localhost because you're running cloud-sql-proxy locally
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"Using local connection via proxy: {DB_HOST}:{DB_PORT}")


def ensure_database_exists():
    """Create database if it doesn't exist"""
    if INSTANCE_CONNECTION_NAME:
        # Cloud Run
        temp_url = f"mysql+pymysql://{DB_USER}:{encoded_pass}@/?unix_socket=/cloudsql/{INSTANCE_CONNECTION_NAME}"
    else:
        # Local
        DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
        DB_PORT = os.getenv("DB_PORT", "3306")
        temp_url = f"mysql+pymysql://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/"

    temp_engine = create_engine(temp_url)

    try:
        with temp_engine.connect() as conn:
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
            conn.execute(text("""
                              CREATE TABLE IF NOT EXISTS addresses
                              (
                                  address_id
                                  CHAR
                              (
                                  36
                              ) NOT NULL,
                                  university_id VARCHAR
                              (
                                  32
                              ) NOT NULL,
                                  street VARCHAR
                              (
                                  255
                              ) NOT NULL,
                                  city VARCHAR
                              (
                                  100
                              ) NOT NULL,
                                  state VARCHAR
                              (
                                  50
                              ) NOT NULL,
                                  postal_code VARCHAR
                              (
                                  20
                              ) NOT NULL,
                                  country VARCHAR
                              (
                                  100
                              ) NOT NULL,
                                  created_at DATETIME
                              (
                                  6
                              ) NOT NULL DEFAULT CURRENT_TIMESTAMP
                              (
                                  6
                              ),
                                  updated_at DATETIME
                              (
                                  6
                              ) NOT NULL DEFAULT CURRENT_TIMESTAMP
                              (
                                  6
                              )
                                  ON UPDATE CURRENT_TIMESTAMP
                              (
                                  6
                              ),
                                  PRIMARY KEY
                              (
                                  address_id
                              ),
                                  KEY idx_addresses_university_id
                              (
                                  university_id
                              )
                                  )
                              """))
            conn.commit()
            print("Table 'addresses' ensured to exist.")
    except Exception as e:
        print(f"Error ensuring tables exist: {e}")
        raise


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