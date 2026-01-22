from pydantic import BaseModel
from typing import Optional


class RawData(BaseModel):
    weapon_id : str  
    weapon_name : str 
    weapon_type : str 
    range_km : int 
    weight_kg : float
    manufacturer  : Optional[str|None]  
    origin_country : str 
    storage_location : str 
    year_estimated : int

class SetData(BaseModel):
    weapon_id : str  
    weapon_name : str 
    weapon_type : str 
    range_km : int 
    weight_kg : float
    manufacturer  : str  
    origin_country : str 
    storage_location : str 
    year_estimated : int
    risk_level : StopIteration