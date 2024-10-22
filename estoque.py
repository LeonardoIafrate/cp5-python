import json
import oracledb
import sqlalchemy
from connection import *

con = connection
cur = con.cursor()


def adiciona_estoque():
    add_qnt = input("Digite a quantidade a ser adicionada ao estoque: ")
    id_livro = input("Digite o ID do livro a ser adicionado: ")
    cur.execute(
    """
    UPDATE ESTOQUE SET Qnt_estoque + :add_qnt WHERE ID_livro = :id_livro 
    """, {"add_qnt": add_qnt, "id_livro": id_livro}
    )
    con.commit()


def remove_estoque():
    rmv_qnt = input("Digite a quantidade a ser removida do estoque: ")
    id_livro = input("Digite o ID do livro a ser removido: ")
    cur.execute(
    """
    UPDATE ESTOQUE SET (Qnt_estoque - :rmv_estoque) WHERE ID_livro = :id_livro   
    """, {"rmv_qnt": rmv_qnt, "id_livro": id_livro}
    )
    con.commit()


def total_estoque():
    cur.execute("SELECT SUM(Qnt_estoque) FROM ESTOQUE")
    con.commit()