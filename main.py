import sys
import asyncio
from src.scale.scale import run_scale_listener
from src.server.loseit import run_losit_listener
import logging
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

if __name__ == "__main__":
    type = str(sys.argv[1])
    if type == "scale":
        asyncio.run(run_scale_listener())
    elif type == "loseit":
        try:
            run_losit_listener()
        except Exception as e:
            logging.error(e)