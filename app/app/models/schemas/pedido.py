from pydantic import BaseModel
from datetime import datetime



class PedidoBase(BaseModel): 
    id: int
    descrition: str
    name: str
    email: str



class PedidoCreate(BaseModel): 
    descrition: str
    name: str
    email: str


class PedidoCreateResponse(BaseModel): 
    id : int
