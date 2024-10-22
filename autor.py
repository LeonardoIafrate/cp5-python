import json
import oracledb
import sqlalchemy
from connection import *

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

def altera_autor():
    id_autor = input("Digite o ID do autor: ")
    nome_autor = input("Digite o nome atual do autor: ")
    cur.execute(
    """
    UPDATE AUTOR SET Nome = :nome_autor WHERE ID_autor = :id_autor
    """, {"id_autor": id_autor, "nome_autor": nome_autor}
    )

def exclui_autor():
    id_autor = input("Digite o ID do autor: ")
    nome_autor = cur.execute("SELECT NOME FROM AUTOR WHERE ID_AUTOR = :id_autor", {"id_autor": id_autor})
    confirmacao = input(f"Você tem certeza que deseja excluir o autor {nome_autor}? (S/N)").upper()
    if confirmacao == "S":
        cur.execute("DELETE FROM AUTOR WHERE ID_autor = :id_autor", id_autor)
    elif confirmacao == "N":
        print("Operação cancelada!")

        