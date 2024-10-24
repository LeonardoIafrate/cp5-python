from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bd_livraria.connection import *
from bd_livraria.livro import adiciona_livro, altera_livro, deleta_livro
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
    
