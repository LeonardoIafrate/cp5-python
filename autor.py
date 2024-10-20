import json
import oracledb
import sqlalchemy
from connection import *

con = connection

cur = con.cursor()

id_autor = input("Digite o ID do autor: ")
nome_autor = input("Digite o nome do autor: ")

def cadastrar_autor():
    cur.execute(
    """
    INSERT INTO AUTOR(ID_autor, Nome)
    VALUES (:id, :nome)
    """, id = id_autor, nome = nome_autor
    )
    con.commit()


def mostra_autor():
    nome_autor = input("Digite o nome do autor: ")
    cur.execute("SELECT * FROM AUTOR WHERE Nome = :nome", nome = nome_autor)

# try:
#     if adiciona_autor():
#         print("Autor cadastrado com sucesso!")
#     else:
#         print("Falha ao cadastrar o autor.")
# except ValueError as e:
#     print("Erro de valor", e)

