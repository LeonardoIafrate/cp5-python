import json
import oracledb
import sqlalchemy
from connection import *

def cadastrae_venda():
    
    #   titulo_livro = input("Digite o título do livro: ")
    # qnt_pag = input("Digite a quantidade de páginas do livro: ")
    # id_autor = input("Digite o ID do autor: ")
    # qnt_estoque = input("Digite a quantidade do livro no estoque: ")
    # preco = input("Digite o preço do livro: ")
    # cur.execute(
    # """
    # INSERT INTO LIVRO( Titulo, Qnt_pag, ID_autor, Qnt_estoque, Preco)
    # VALUES(: :titulo_livro, :qnt_pag, :id_autor, :qnt_estoque, :preco)
    # """,{"titulo_livro": titulo_livro, "qnt_pag": qnt_pag, "id_autor":id_autor, "qnt_estoque": qnt_estoque} 
    # )
