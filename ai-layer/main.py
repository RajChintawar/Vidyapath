# ai-layer/planning/main.py
from common.db import db
# print("Collections:", db.list_collection_names())

from common.db import db

print("CONNECTED DATABASE NAME:", db.name)
print("ALL COLLECTIONS:", db.list_collection_names())

print("\n--- USERS COLLECTION CONTENT ---")
users = list(db.users.find({}))
print("Users found:", len(users))
for u in users:
    print(u)





def test_db_connection():
    users_count = db.users.count_documents({})
    tasks_count = db.tasks.count_documents({})

    print("DB connected successfully")
    print("Users count:", users_count)
    print("Tasks count:", tasks_count)

if __name__ == "__main__":
    test_db_connection()