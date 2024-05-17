from pydantic import BaseModel
from datetime import datetime



class PedidoBase(BaseModel): 
    id: int
    descrition: str


class PedidoCreate(BaseModel): 
    descrition: str


class PedidoCreateResponse(BaseModel): 
    id : int
