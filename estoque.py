import json
import oracledb
import sqlalchemy
from connection import *

con = connection
cur = con.cursor()


rmv_qnt = input("Digite a quantidade a ser removida do estoque: ")

def adiciona_estoque():
    add_qnt = input("Digite a quantidade a ser adicionada ao estoque: ")
    id_livro = input("Digite o ID do livro a ser adicionado: ")
    cur.execute(
    """
    UPDATE ESTOQUE SET Qnt_estoque + :add_qnt WHERE ID_livro = :id_livro 
    """, {"add_qnt": add_qnt, "id_livro": id_livro}
)