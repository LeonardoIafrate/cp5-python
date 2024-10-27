from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from bd_livraria.connection import *
from bd_livraria.livro import cadastrar_livro, deleta_livro
from bd_livraria.autor import cadastrar_autor, altera_autor, exclui_autor
from bd_livraria.estoque import adiciona_estoque, remove_estoque, total_estoque
from bd_livraria.genero import cadastra_genero, exclui_genero, altera_genero
from bd_livraria.venda import relatorio_venda


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

class Autor(BaseModel):
    nome: str

class LivroVenda(BaseModel):
    id_livro: int
    quantidade: int

class VendaRequest(BaseModel):
    nome_cliente: str
    livros: list[LivroVenda]

class UpdateLivroVenda(BaseModel):
    id_livro: Optional[int] = None
    quantidade: Optional[int] = None

@app.get("/get-livro/{id_livro}")
async def get_livro(id_livro: int):
    cur.execute("SELECT * FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
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


@app.get("/get-book/{titulo_livro}")
async def mostra_livro(titulo_livro : str):
    titulo = f"%{titulo_livro.upper()}%"

    try:
        cur.execute("SELECT * FROM LIVRO WHERE Titulo LIKE :titulo", {"titulo": titulo})
        livros = cur.fetchall()

        livros_encontrados = []
        for livro in livros:
            livro_dict = {
                "ID do livro": livro[0],
                "Título do livro": livro[1],
                "Quantidade de páginas": livro[2],
                "ID do autor": livro[3],
                "Preço do livro": livro[4],
                "Gênero do livro": livro[5]
            }
            livros_encontrados.append(livro_dict)
        return {"Livros": livros_encontrados}
    except HTTPException as e:
        return{"status_code": "500", "detail": f"Erro ao buscar livro: {str(e)}"}
    

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


@app.delete("/deleta-livro/{id_livro}")
async def delet_livro(id_livro: int):
    deleta_livro(id_livro)


@app.get("/get-autor/{id_autor}")
async def get_autor(id_autor: int):
    cur.execute("SELECT * FROM AUTOR WHERE ID_autor = :id_autor", {"id_autor": id_autor})
    autor = cur.fetchone()
    if autor:
        autor_dict = {
            "ID do autor": autor[0],
            "Nome do autor": autor[1],
        }
        return autor_dict
    else:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    

@app.get("/get-author/{nome_autor}")
async def mostra_autor(nome_autor: str):
    nome = f"%{nome_autor.upper()}%"
    
    try:
        cur.execute("SELECT * FROM AUTOR WHERE Nome LIKE :nome", {"nome": nome})
        autores = cur.fetchall()

        autores_encontrados = []
        for autor in autores:
            autor_dict = {
                "ID do autor": autor[0],
                "Nome do autor": autor[1]
            }
            autores_encontrados.append(autor_dict)
        return {"Autores": autores_encontrados}
    except HTTPException as e:
        return {"status_code": "500", "detail": f"Autor não encontrado {str(e)}"}
    

@app.put("/update-autor/{id_autor}")
async def update_autor(id_autor: int, autor: Autor):
    resultado = altera_autor(id_autor, autor.nome )
    return resultado

@app.post("/cadastrar-autor/")
async def criar_novo_autor(autor: Autor):
    cadastro = cadastrar_autor(autor.nome)
    return cadastro

#colocar exclui autor aqui e apagar comentario dps

###

@app.put("/adiciona-estoque/{id_livro}")
async def adiciona_ao_estoque(id_livro: int, qnt: int):
    resultado = adiciona_estoque(id_livro, qnt)
    return resultado


@app.put("/remove-estoque/{id_livro}")
async def remove_do_estoque(id_livro: int, qnt: int):
    resultado = remove_estoque(id_livro, qnt)
    return resultado


@app.get("/total-estoque")
async def total_livros_estoque():
    resultado = total_estoque()
    return {"Message" : f"Quantidade total de livros no estoque: {resultado}"}

@app.get("/relatorio-venda/{id_venda}")
async def sale_report(id_venda: int):
    resultado = relatorio_venda(id_venda)
    return resultado

@app.post("/cadastrar_venda/")
async def cadastrar_venda(venda_request: VendaRequest):
    try:
        response = cadastra_venda_livros(venda_request.nome_cliente, venda_request.livros)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


async def cadastra_venda_livros(nome_cliente: str, livros: list):
    data_venda = datetime.now().strftime("%d-%m-%Y")
    id_venda = cur.var(oracledb.NUMBER)

    try:
        cur.execute(
            """
            INSERT INTO VENDA(DATA_VENDA, NOME_CLIENTE)
            VALUES (TO_DATE(:DATA_VENDA, 'DD-MM-YYYY'), :NOME_CLIENTE)
            RETURNING ID_VENDA INTO :id_venda
            """, 
            {"DATA_VENDA": data_venda, "NOME_CLIENTE": nome_cliente, "id_venda": id_venda}
        )
        con.commit()
        
        id_venda = id_venda.getvalue()[0]

        for livro in livros:
            id_livro = livro.id_livro
            quantidade = livro.quantidade
            cadastra_venda(id_venda, id_livro, quantidade)

        return {"Message": f"Venda cadastrada com sucesso, ID da venda: {id_venda}, data venda: {data_venda}"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar venda: {str(e)}")
        

async def cadastra_venda(id_venda: int, id_livro: int, qnt: int):
    cur.execute(
        """
        INSERT INTO VENDA_LIVROS(ID_VENDA, ID_LIVRO, QUANTIDADE)
        VALUES (:ID_VENDA, :ID_LIVRO, :QUANTIDADE)
        """, 
        {"ID_VENDA": id_venda, "ID_LIVRO": id_livro, "QUANTIDADE": qnt}
    )
    con.commit()

@app.put("/altera-venda-livro/{id_venda}")
async def update_venda_livro(id_venda: int, id_livro: int, lvenda: UpdateLivroVenda):
    cur.execute("SELECT ID_VENDA FROM VENDA WHERE ID_VENDA = :id_venda", {"id_venda": id_venda})
    venda_cadastrada = cur.fetchone()

    if venda_cadastrada is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    cur.execute("SELECT ID_LIVRO FROM VENDA_LIVROS WHERE ID_VENDA = :id_venda AND ID_LIVRO = :id_livro", {"id_venda": id_venda, "id_livro": id_livro})
    venda_livro_cadastrada = cur.fetchone()

    if venda_livro_cadastrada is None:
        raise HTTPException(status_code=404, detail="Este livro não faz parte dessa venda")
    
    try:
        if lvenda.id_livro != None:
            cur.execute("UPDATE VENDA_LIVROS SET ID_LIVRO = :new_id_livro WHERE ID_LIVRO = :id_livro AND ID_VENDA = :id_venda", {"new_id_livro": lvenda.id_livro, "id_livro": id_livro, "id_venda": id_venda})
        
        if lvenda.quantidade != None:
            cur.execute("UPDATE VENDA_LIVROS SET QUANTIDADE = :quantidade WHERE ID_LIVRO = :id_livro AND ID_VENDA = :id_venda", {"quantidade": lvenda.quantidade, "id_livro": id_livro, "id_venda": id_venda})
        con.commit()
        
        return {"Message": "Livro da venda alterado com sucesso"}
    except oracledb.IntegrityError:
        return {"Error": "Livro não cadastrado"}
    except Exception as e:
        return {"Error": f"Erro ao alterar livro {str(e)}"}
    
