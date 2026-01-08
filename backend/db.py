from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ai_firewall"]

alerts_collection = db["alerts"]
blocked_ips_collection = db["blocked_ips"]
users_collection = db["users"]
