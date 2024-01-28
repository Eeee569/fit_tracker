from src.scale.normalizer import check_scale_value
from settings import Settings
from src.scale.reader import ScaleReader
from src.db import DB
import time
import asyncio
import logging

logging.basicConfig(level=logging.INFO)



def populate_scale_data(database: DB):
    if database.db["scaleData"].count_documents({}) == 0:
        database.insert(collection="scaleData", data={"impedance": Settings.first_db_value_fill[0], "weight": Settings.first_db_value_fill[1], "date": int(time.time())})

async def run_scale_listener():
    reader = ScaleReader()

    database = DB()

    past_scale_tuple = (0,0)

    populate_scale_data(database)

    while True:
        try:
            scale_tuple = await reader.run()


            logging.info(scale_tuple)

            if scale_tuple == past_scale_tuple:
                continue

            if not check_scale_value(database, scale_tuple):
                continue

            impedance, weight = scale_tuple

            database.insert(
                "scaleData",
                {"impedance": impedance, "weight": weight, "date": int(time.time())},
            )

            past_scale_tuple = scale_tuple
        except Exception as e:
            database.report_error(Settings.device, str(e))


if __name__ == "__main__":
    asyncio.run(run_scale_listener())


