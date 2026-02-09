# ai-layer/common/db.py
from pymongo import MongoClient
from common.config import MONGO_URI, DB_NAME

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["academic_planner"]