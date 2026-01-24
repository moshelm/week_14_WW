from fastapi import APIRouter,UploadFile,File
import pandas as pd
from io import BytesIO
from .models import DataF
from .db import insert_db,init_table,init_database

router = APIRouter()

# init_database()
# init_table()

@router.post('/upload')
def get_csv(file:UploadFile=File(...)):
    
    df = read_csv(file)
    clean_none(df)
    create_risk_level_column(df)
    data = DataF(records=df.to_dict(orient='records'))
    insert_db(data)
    return {"status": "success",'number records':len(data.records)}


def read_csv(file:UploadFile)-> pd.DataFrame:
    contents = file.file.read()
    data = BytesIO(contents)
    return pd.read_csv(data)

def clean_none(df:pd.DataFrame)->pd.DataFrame:
    df.fillna(value='Unknown',inplace=True)

def create_risk_level_column(df:pd.DataFrame)->pd.DataFrame:
    df['risk_level'] = df['range_km'].map(risk_category)

def risk_category(value):
    if value <= 20:
        return 'low'
    elif 100 >= value > 20:
        return 'medium'
    elif 300 >= value > 100:
        return 'high'
    else:
        return 'extreme'
    