from fastapi import HTTPException
import json
import oracledb
import sqlalchemy
from bd_livraria.connection import *

con = connection

def total_estoque():
    cur.execute("SELECT SUM(Qnt_estoque) FROM ESTOQUE")
    total = cur.fetchone()[0]
    return total if total is not None else 0


def adiciona_quantidade(id_livro, qnt):
    if (total_estoque() + qnt) > 25000:
        raise HTTPException(status_code=400, detail="O limite do estoque é de 25000")
    else:
        cur.execute(
            """
            UPDATE ESTOQUE SET Qnt_estoque = Qnt_estoque + :add_qnt WHERE ID_livro = :id_livro 
            """, {"add_qnt": qnt, "id_livro": id_livro}
        )
        con.commit()
        return {"Message": "Quantidade adicionada com sucesso!"}


def adiciona_estoque(id_livro: int, qnt: int):
    cur.execute("SELECT ID_livro FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
    livro_cadastrado = cur.fetchone()

    if livro_cadastrado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    try:
        if livro_cadastrado:
            cur.execute("SELECT Qnt_estoque FROM ESTOQUE WHERE ID_livro = :id_livro", {"id_livro": id_livro})
            livro_no_estoque = cur.fetchone()
            if livro_no_estoque:
                adiciona_quantidade(id_livro, qnt)
                return {"Message": "Quantidade adicionada com sucesso!"}
            else:
                cur.execute(
                """
                INSERT INTO ESTOQUE(ID_livro, Qnt_estoque)
                VALUES(:id_livro, 0)
                """, {"id_livro": id_livro}
                )
                con.commit()
                adiciona_quantidade(id_livro, qnt)
                return {"Message": "Quantidade adicionada com sucesso!"}
    except KeyError as e:
        print("Erro ao adicionar estoque: ", e)


def remove_quantidade(id_livro: int, qnt: int):
    cur.execute("SELECT Qnt_estoque FROM ESTOQUE WHERE ID_livro = :id_livro", {"id_livro": id_livro})
    quantidade_atual = cur.fetchone()[0]
    
    if (quantidade_atual - qnt) < 0:
        raise HTTPException(status_code=400, detail="Um livro não pode ter uma quantidade negativa no estoque")
    else:
        cur.execute(
        """
        UPDATE ESTOQUE SET Qnt_estoque = (Qnt_estoque - :rmv_qnt) WHERE ID_livro = :id_livro
        """, { "id_livro": id_livro, "rmv_qnt": qnt})
        con.commit()
        return {"Message": "Quantidade removida com sucesso!"}
    
    


def remove_estoque(id_livro: int, qnt: int):
    cur.execute("SELECT ID_livro FROM ESTOQUE WHERE ID_livro = :id_livro", {"id_livro": id_livro})
    livro_cadastrado = cur.fetchone()
    
    if livro_cadastrado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    try:    
        if livro_cadastrado:
            remove_quantidade(id_livro,qnt)
            return{"Message": "Quantidade removida com sucesso"}
    except KeyError as e:
        return{"Error": f"Erro ao remover do estoque, {str(e)}"}
