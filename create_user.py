from databasesetup import SessionLocal
from schema import User

db = SessionLocal()

users = [
    User(email="hr@company.com", password="123", role="HR", dept_id=1),
    User(email="manager@company.com", password="123", role="Manager", dept_id=1),
    User(email="leader@company.com", password="123", role="Leader", dept_id=1),
]

for u in users:
    existing = db.query(User).filter_by(email=u.email).first()
    if not existing:
        db.add(u)

db.commit()
db.close()

print("Users created successfully")