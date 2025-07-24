import os
os.environ["DATABASE_URL"] = "sqlite:///local_llama_offline.db"

from local_llama.models import *
from sqlmodel import create_engine, SQLModel

# Create engine
engine = create_engine("sqlite:///local_llama_offline.db")

# Create all tables
SQLModel.metadata.create_all(engine)

print("Created offline SQLite database with all tables")
