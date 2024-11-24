# models.py
from pydantic import BaseModel

class Filme(BaseModel):
    titulo: str
    ano: int
    genero: str
    diretor: str
