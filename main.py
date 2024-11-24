from fastapi import FastAPI, HTTPException
from typing import List
from models import Filme
from database import db

app = FastAPI()

# Endpoint para criar um novo filme
@app.post("/filmes/", response_model=dict)
def criar_filme(filme: Filme):
    query = """
    CREATE (f:Filme {titulo: $titulo, ano: $ano, genero: $genero, diretor: $diretor})
    RETURN f
    """
    db.query(query, {"titulo": filme.titulo, "ano": filme.ano, "genero": filme.genero, "diretor": filme.diretor})
    return {"message": "Filme criado com sucesso!"}

# Endpoint para ler todos os filmes
@app.get("/filmes/", response_model=List[Filme])
def ler_filmes():
    query = "MATCH (f:Filme) RETURN f.titulo AS titulo, f.ano AS ano, f.genero AS genero, f.diretor AS diretor"
    filmes = db.query(query)
    
    filmes_lista = []
    for record in filmes:
        filmes_lista.append(Filme(titulo=record["titulo"], ano=record["ano"], genero=record["genero"], diretor=record["diretor"]))
    
    return filmes_lista

# Endpoint para ler um filme específico por título
@app.get("/filmes/{titulo}", response_model=Filme)
def ler_filme(titulo: str):
    query = "MATCH (f:Filme {titulo: $titulo}) RETURN f.titulo AS titulo, f.ano AS ano, f.genero AS genero, f.diretor AS diretor"
    result = db.query(query, {"titulo": titulo})
    if result:
        # Aqui já consumimos todos os resultados
        record = result[0]  # Acessamos o primeiro resultado
        return Filme(titulo=record["titulo"], ano=record["ano"], genero=record["genero"], diretor=record["diretor"])
    else:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

# Endpoint para atualizar um filme
@app.put("/filmes/{titulo}", response_model=dict)
def atualizar_filme(titulo: str, filme: Filme):
    query = """
    MATCH (f:Filme {titulo: $titulo})
    SET f.ano = $ano, f.genero = $genero, f.diretor = $diretor
    RETURN f
    """
    result = db.query(query, {"titulo": titulo, "ano": filme.ano, "genero": filme.genero, "diretor": filme.diretor})
    if result:
        return {"message": "Filme atualizado com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

# Endpoint para deletar um filme
@app.delete("/filmes/{titulo}", response_model=dict)
def deletar_filme(titulo: str):
    query = "MATCH (f:Filme {titulo: $titulo}) DELETE f"
    result = db.query(query, {"titulo": titulo})
    if result:
        return {"message": "Filme deletado com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
