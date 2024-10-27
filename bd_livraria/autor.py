from fastapi import HTTPException
import oracledb
from bd_livraria.connection import *

con = connection

cur = con.cursor()


def cadastrar_autor(id_autor: int, nome_autor: str):
    try:
        cur.execute(
        """
        INSERT INTO AUTOR(Nome)
        VALUES (:nome)
        """, {"nome": nome_autor}
        )
        con.commit()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar autor: {str(e)}")


def mostra_autor():
    nome_autor = input("Digite o nome do autor: ")
    cur.execute("SELECT * FROM AUTOR WHERE Nome = :nome", {"nome": nome_autor})

def altera_autor(id_autor: int, nome_autor: str):
    cur.execute("SELECT * FROM AUTOR WHERE ID_autor = :id_autor", {"id_autor": id_autor})
    autor = cur.fetchone()
    
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    
    try:
        cur.execute(
        """
        UPDATE AUTOR SET Nome = :nome_autor WHERE ID_autor = :id_autor
        """, {"id_autor": id_autor, "nome_autor": nome_autor}
        )
        con.commit()
        return {"Message": "Autor alterado com sucesso"}
    except Exception as e:
        return {"Erro": f"Um erro inesperado aconteceu, {str(e)}"}


def exclui_autor(id_autor: int):
    cur.execute("SELECT * FROM AUTOR WHERE ID_autor = :id_autor", {"id_autor": id_autor})
    autor = cur.fetchone()
    if autor is None: 
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    
    try:
        cur.execute(
        """
        DELETE FROM AUTOR WHERE ID_autor = :id_autor
        """, {"id_autor":id_autor})
        con.commit()
        return {"Message":"Autor excluido com sucesso"}
    except Exception as e:
        return {"Erro": f"Um erro inesperado aconteceu, {str(e)}"}

        