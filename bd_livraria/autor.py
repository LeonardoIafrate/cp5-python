import json
from fastapi import HTTPException
import oracledb
from bd_livraria.connection import *

con = connection

cur = con.cursor()


def cadastrar_autor():
    nome_autor = input("Digite o nome do autor: ")
    cur.execute(
    """
    INSERT INTO AUTOR(Nome)
    VALUES (:nome)
    """, {"nome": nome_autor}
    )
    con.commit()


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


def exclui_autor():
    id_autor = input("Digite o ID do autor: ")
    nome_autor = cur.execute("SELECT NOME FROM AUTOR WHERE ID_AUTOR = :id_autor", {"id_autor": id_autor})
    confirmacao = input(f"Você tem certeza que deseja excluir o autor {nome_autor}? (S/N)").upper()
    if confirmacao == "S":
        cur.execute("DELETE FROM AUTOR WHERE ID_autor = :id_autor", id_autor)
    elif confirmacao == "N":
        print("Operação cancelada!")

        