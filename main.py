import sys
import asyncio
from src.scale.scale import run_scale_listener

if __name__ == "__main__":
    type = str(sys.argv[1])
    if type == "scale":
        asyncio.run(run_scale_listener())
