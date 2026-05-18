import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/bi_database")
engine = create_engine(DATABASE_URL)

# Secure dummy schema presentation string provided to the Agent
SCHEMA_DESCRIPTION = """
Table: daily_sales
Columns:
  - id (INTEGER, Primary Key)
  - product_name (VARCHAR)
  - category (VARCHAR)
  - units_sold (INTEGER)
  - revenue (NUMERIC)
  - sale_date (DATE)
"""
