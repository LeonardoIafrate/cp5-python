import json
import oracledb
import sqlalchemy
from autor import *

def adiciona_livro():
    autor_cadastrado = input("O autor do livro já possuí cadastro? (S/N) \n").upper()
    if autor_cadastrado == "S":
        sabe_ID = input("Você já sabe o ID do autor? (S/N) \n").upper()
        if sabe_ID == "S":
            input("Digite o ID do autor: ")
            cadastrar_livro()
        elif sabe_ID == "N":
            mostra_autor()
            cadastrar_livro()
        else:
            print("Opção inválida. Tente novamente.")
    elif autor_cadastrado == "N":
        cadastrar_autor()
        cadastrar_livro()
    else:
        print("Opção inválida. Tente novamente.")



def cadastrar_livro():
    ID_livro = input("Digite o ID do livro: ")
    Titulo_livro = input("Digite o título do livro: ")
    Qnt_pag = input("Digite a quantidade de páginas do livro: ")
    ID_autor = input("Digite o ID do autor: ")
    cur.execute(
    """
    INSERT INTO LIVRO(ID_LIVRO, TITULO, QTD_PAGINA, autor_ID-autor)
    VALUES(:id_livro, :titulo_livro, :qnt_pag, :id_autor)
    """, id_livro = ID_livro, titulo_livro = Titulo_livro, qnt_pag = Qnt_pag, id_autor = ID_autor 
    )    

def cadastra_genero():
    genero = input("Digite o gênero que deseja cadastrar")
