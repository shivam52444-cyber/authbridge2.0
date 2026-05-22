# database.py
# databasesetup.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# ---------------------------------------
# DATABASE URL (Render PostgreSQL)
# ---------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment")

# 🔥 Fix for Render (important)
# sometimes url starts with postgres:// instead of postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ---------------------------------------
# ENGINE
# ---------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # avoids stale connections
)

# ---------------------------------------
# SESSION
# ---------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------
# BASE
# ---------------------------------------
Base = declarative_base()