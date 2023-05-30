import time

from src.db import DB
from settings import Settings

def check_scale_value(database: DB, scale_value: tuple) -> bool:
    impedance, weight = scale_value
    if impedance == 0 or weight == 0:
        return False
    last_scale_value = database.findOne("scaleData", [("date", -1)])
    if time.time() - last_scale_value['date'] < Settings.time_interval:
        return False
    if not last_scale_value:
        raise Exception("No scale data found in normalization")
    if abs(last_scale_value['impedance'] - impedance) > Settings.impedance_interval:
        return False
    if abs(last_scale_value['weight'] - weight) > Settings.weight_interval:
        return False
    return True
