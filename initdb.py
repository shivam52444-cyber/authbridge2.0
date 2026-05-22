from databasesetup import engine
from schema import Base

Base.metadata.create_all(bind=engine)
print("Database initialized")