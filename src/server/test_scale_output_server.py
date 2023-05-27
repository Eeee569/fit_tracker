from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
import uvicorn

class Item(BaseModel):
    output_list : list


app = FastAPI()


def test_as_bytes(imt_list):
    print(f'input: {imt_list}')
    str_out = ''
    for itm in imt_list:
        str_out += str(itm)
    print(f'test_change: {str_out}')

@app.post("/items/")
async def get_items(item: Item):

    test_as_bytes(item.output_list)

    return {"status": 'ya'}

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')


#1001100111001100011001100011101110011001110011000110011100111001110011000110001100011000110001100011