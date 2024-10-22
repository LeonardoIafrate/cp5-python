# alteraços concluidas

import json
import oracledb
import sqlalchemy
from autor import *

def adiciona_livro():
    try:
        autor_cadastrado = input("O autor do livro já possuí cadastro? (S/N) \n").upper()
        if autor_cadastrado == "S":
            sabe_ID = input("Você já sabe o ID do autor? (S/N) \n").upper()
            if sabe_ID == "S":
                cadastrar_livro()
            elif sabe_ID == "N":
                mostra_autor()
                cadastrar_livro()
            raise ValueError("Opção inválida. Tente novamente.")
        elif autor_cadastrado == "N":
            cadastrar_autor()
            mostra_autor()
            cadastrar_livro()
        raise ValueError("Opção inválida. Tente novamente.")
    except ValueError as e:
        print("Erro", e)


def cadastrar_livro():
    titulo_livro = input("Digite o título do livro: ")
    qnt_pag = input("Digite a quantidade de páginas do livro: ")
    id_autor = input("Digite o ID do autor: ")
    qnt_estoque = input("Digite a quantidade do livro no estoque: ")
    preco = input("Digite o preço do livro: ")
    cur.execute(
    """
    INSERT INTO LIVRO( Titulo, Qnt_pag, ID_autor, Qnt_estoque, Preco)
    VALUES(: :titulo_livro, :qnt_pag, :id_autor, :qnt_estoque, :preco)
    """,{"titulo_livro": titulo_livro, "qnt_pag": qnt_pag, "id_autor":id_autor, "qnt_estoque": qnt_estoque} 
    )


def altera_livro():
    id_livro = input("Digite o id do livro que deseja alterar: ")
    print("Se não quiser alterar as informações a seguir, copie a informação atual")
    titulo = input("Digite o atual titulo do livro: ")
    qnt_pag = input("Digite a atual quantidade de páginas do livro: ")
    id_autor = input("Digite o atual id do autor: ")
    qnt_estoque = input("Digite a atual quantidade do livro no estoque: ")
    preco = input("Digite o atual valor do preço: ")
    cur.execute(
    """
    UPDATE LIVRO SET Titulo = :titulo, Qnt_pag = :qnt_pag, ID_autor = :id_autor, Qnt_estoque = :qnt_estoque, Preco = :preco
    WHERE ID_livro = :id_livro
    """, {"id_livro": id_livro,"titulo": titulo, "qnt_pagina": qnt_pag, "id_autor": id_autor, "qnt_estoque": qnt_estoque, "preco": preco}
    )
    con.commit()


def deleta_livro():
    id_livro = input("Digite o id do livro que deseja excluir: ")
    nome_livro = cur.execute("SELECT Titulo FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
    confirmacao = input(f"Tem certeza que deseja excluir o livro {nome_livro}? (S/N)").upper()
    if confirmacao == "S":
        exclui = cur.execute(
            """
            DELETE FROM LIVRO WHERE ID_livro = :id_livro
            """, {"id_livro": id_livro})
        if exclui:
            print("Livro excluido com sucesso.")
        else:
            print("Erro ao excluir livro.")
    elif confirmacao == "N":
        print("Operação cancelada.")