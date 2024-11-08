from typing import Union
from fastapi import FastAPI

## Extra Library
import numpy as np
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/material_comp")
def material_comp():
    fname='assets/materials_compositions.csv'
    cols=['compositions', 'SMP', 'WMP', 'WPC', 'Stab_a', 'Stab_b', 'Cocoa_a', 'Cocoa_b', 'Sugar', 'Minor']
    df_compositions = pd.read_csv(fname,sep='\t', names=cols, index_col='compositions', skiprows=1)
    return df_compositions.to_json()

@app.get("/recipies")
def recipies():
    fname='assets/recipies.csv'
    df_recepies = pd.read_csv(fname,sep='\t',names=['compositions','Chocolate','Plain','Strawberry'],index_col='compositions',skiprows=1)
    return df_recepies.to_json()