from pymongo import MongoClient
from settings import Settings
import time

class DB:

    def __init__(self):
        self.client = MongoClient(Settings.db_path)
        self.db = self.client["fitdb"]

    def insert(self, collection: str, data: dict) -> None:
        self.db[collection].insert_one(data)

    def findOne(self, collection: str, sort: list) -> dict:
        return self.db[collection].find_one(sort=sort)

    def report_error(self, device: str, error: str) -> None:
        self.insert("error", {"device": device, "error": error, "date": int(time.time())})

    def close(self) -> None:
        self.client.close()
