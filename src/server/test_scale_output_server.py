from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    ouput_list : list


app = FastAPI()



def test_as_bytes(imt_list):
    print(f'input: {imt_list}')
    str_out = ''
    for itm in imt_list:
        str_out += itm
    print(f'test_change: {str_out}')

@app.post("/items/")
async def get_items(item: Item):

    test_as_bytes(item.ouput_list)

    return {"status": 'ya'}
