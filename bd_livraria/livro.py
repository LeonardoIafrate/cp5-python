import json
import oracledb
from bd_livraria.autor import *
from typing import Optional


def cadastrar_livro(titulo_livro: str, qnt_pag: int, id_autor: int, preco: float, genero: str):
    try:
        cur.execute(
        """
        INSERT INTO LIVRO(Titulo, Qnt_pag, ID_autor, Preco, Genero)
        VALUES(:titulo_livro, :qnt_pag, :id_autor, :preco, :genero)
        """,{"titulo_livro": titulo_livro, "qnt_pag": qnt_pag, "id_autor":id_autor, "preco": preco, "genero": genero} 
        )
        con.commit()
        return {"Message": "Livro cadastrado com sucesso!"}
    except oracledb.DatabaseError as e:
        return {"Error": f"Erro ao cadastrar o livro: {str(e)}"}

        
# def altera_livro(id_livro: int, titulo: Optional[str], qnt_pag: Optional[int], id_autor: Optional[int], preco: Optional[float], genero: Optional[str]):
#     try:
#         alteracoes = []
#         parametros = {"id_livro": id_livro}

#         if titulo != None:
#             alteracoes.append("Titulo = :titulo")
#             parametros["titulo"] = titulo

#         if qnt_pag != None:
#             alteracoes.append("Qnt_pag = :qnt_pag")
#             parametros["qnt_pag"] = qnt_pag

#         if id_autor != None:
#             alteracoes.append("ID_autor = :id_autor")
#             parametros["id_autor"] = id_autor

#         if preco != None:
#             alteracoes.append("Preco = :preco")
#             parametros["preco"] = preco

#         if genero != None:
#             alteracoes.append("Genero = :genero")
#             parametros["genero"] = genero

#         query = f"UPDATE LIVRO SET {', '.join(alteracoes)} WHERE ID_livro = :id_livro"

#         cur.execute(query, parametros)
#         con.commit()
#         return{"Message": "Livro alterado com sucesso"}
    
#     except KeyError:
#         return {"Message": f"Erro ao alterar o livro: ID não encontrado"}


def deleta_livro(id_livro: int):
    try:
        cur.execute("SELECT Titulo FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
        livro = cur.fetchone()
        if livro:
            cur.execute(
            """
            DELETE FROM LIVRO WHERE ID_livro = :id_livro
            """, {"id_livro": id_livro})
            con.commit()
            return {"Message": "Livro excluído com sucesso"}
    except KeyError:
        return {"Message": "Livro não cadastrado"}