from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from bd_livraria.connection import *
from bd_livraria.livro import cadastrar_livro, altera_livro, deleta_livro
from bd_livraria.autor import cadastrar_autor, altera_autor, exclui_autor
from bd_livraria.estoque import adiciona_estoque, remove_estoque
from bd_livraria.genero import cadastra_genero, exclui_genero, altera_genero

app = FastAPI()

class Livro(BaseModel):
    titulo_livro: str
    qnt_pag: int
    id_autor: int
    preco: float
    genero: str

class UpdateLivro(BaseModel):
    titulo_livro: Optional[str] = None
    qnt_pag : Optional[int] = None
    id_autor: Optional[int] = None
    preco: Optional[float] = None
    genero: Optional[str] = None

@app.get("/get-livro/{titulo_livro}")
async def mostra_livro(titulo_livro : str):
    
    cur.execute("SELECT ID_livro, Titulo, Qnt_pag, ID_autor, Preco, Genero FROM LIVRO WHERE Titulo = :titulo", {"titulo": titulo_livro})
    livro = cur.fetchone()

    if livro:
        livro_dict = {
            "ID do livro": livro[0],
            "Título do livro": livro[1],
            "Quantidade de páginas": livro[2],
            "ID do autor": livro[3],
            "Preço do livro": livro[4],
            "Gênero do livro": livro[5]
        }
        return livro_dict
    else:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    

@app.post("/cadastrar-livro/")
async def cadastrar_novo_livro(livro: Livro):
    resultado = cadastrar_livro(
        livro.titulo_livro,
        livro.qnt_pag,
        livro.id_autor,
        livro.preco,
        livro.genero
    )
    return resultado

@app.put("/altera-livro/{id_livro}")
async def update_livro(id_livro: int, livro: UpdateLivro):
    cur.execute("SELECT ID_livro FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
    livro_existe = cur.fetchone()

    if livro_existe is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    try:
        if livro.titulo_livro != None:
            cur.execute("UPDATE LIVRO SET Titulo = :titulo_livro WHERE ID_livro = :id_livro", {"titulo_livro": livro.titulo_livro, "id_livro": id_livro})

        if livro.qnt_pag != None:
            cur.execute("UPDATE LIVRO SET Qnt_pag = :qnt_pag WHERE ID_livro = :id_livro", {"qnt_pag": livro.qnt_pag, "id_livro": id_livro} )

        if livro.id_autor != None:
            cur.execute("UPDATE LIVRO ID_autor = :id_autor WHERE ID_livro = :id_livro", {"id_autor": livro.id_autor, "id_livro": id_livro})

        if livro.preco != None:
            cur.execute("UPDATE LIVRO SET Preco = :preco WHERE ID_livro = :id_livro", {"preco": livro.preco, "id_livro": id_livro})

        if livro.genero != None:
            cur.execute("UPDATE LIVRO SET Genero = :genero WHERE ID_livro = :id_livro", {"genero": livro.genero, "id_livro": id_livro})

        con.commit()
        return {"Message": "Livro alterado com sucesso!"}
    except Exception as e:
        return {"Message": "Erro ao alterar livro", "Error": str(e)}