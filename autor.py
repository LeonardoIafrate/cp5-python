import json
import oracledb
import sqlalchemy

dsn_str = oracledb.makedsn("oracle.fiap.com.br", 1521, "ORCL")
con = oracledb.connect(user='rm558831', password='030405', dsn=dsn_str)

cur = con.cursor()

id_autor = input("Digite o ID do autor: ")
nome_autor = input("Digite o nome do autor: ")

def cadastrar_autor():
    cur.execute(
    """
    INSERT INTO AUTOR("ID-autor", NOME)
    VALUES (:id, :nome)
    """, id = id_autor, nome = nome_autor
    )
    con.commit()


def mostra_autor():
    nome_autor = input("Digite o nome do autor: ")
    cur.execute("SELECT * FROM AUTOR WHERE NOME = :nome", nome = nome_autor)

# try:
#     if adiciona_autor():
#         print("Autor cadastrado com sucesso!")
#     else:
#         print("Falha ao cadastrar o autor.")
# except ValueError as e:
#     print("Erro de valor", e)

