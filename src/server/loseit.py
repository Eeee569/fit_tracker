from src.server.gmail import Gmail
from settings import Settings
from src.db import DB
import time
import csv

def run_losit_listener() -> None:
    run_time = time.time()

    while True:

        if time.time() - run_time > Settings.time_interval*3600:
            run()
            run_time = time.time()
        else:
            time.sleep(60)

def run() -> None:
    gmail_data = get_gmail_stats(Settings.email)
    db = DB()
    for data in gmail_data[1]:
        save_to_db(db, data)
    db.close()

def get_gmail_stats(email: str) -> tuple:
    gmail = Gmail()
    csvs = gmail.get_csvs(email)
    return csvs[0], csvs[1]

def save_to_db(db: DB, data: bytes) -> None:
    data = data.decode('utf-8').splitlines()
    reader = csv.DictReader(data)
    for line in reader:
        line.pop('Icon', None)
        db.insert("loseitData", line)


if __name__ == "__main__":
    run()