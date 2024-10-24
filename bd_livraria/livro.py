# alteraços concluidas

import json
import oracledb
from bd_livraria.autor import *



def cadastrar_livro(titulo_livro: str, qnt_pag: int, id_autor: int, preco: float, genero: str):
    try:
        cur.execute(
        """
        INSERT INTO LIVRO(Titulo, Qnt_pag, ID_autor, Preco, Genero)
        VALUES(:titulo_livro, :qnt_pag, :id_autor, :preco, :genero)
        """,{"titulo_livro": titulo_livro, "qnt_pag": qnt_pag, "id_autor":id_autor, "preco": preco, "genero": genero} 
        )
        con.commit()
        return {"Message": "Livro cadastrado com sucesso!"}
    except oracledb.DatabaseError as e:
        return {"Error": f"Erro ao cadastrar o livro: {str(e)}"}

        
def altera_livro():
    try:
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
        if cur.rowcount == 0:
            raise KeyError("O livro não está cadastrado na tabela.")
        con.commit()
    except KeyError as e:
        print("Erro ao alterar o livro: ", e)


def deleta_livro():
    try:
        id_livro = input("Digite o id do livro que deseja excluir: ")
        cur.execute("SELECT Titulo FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
        livro = cur.fetchone()
        confirmacao = input(f"Tem certeza que deseja excluir o livro {livro}? (S/N)").upper()
        if livro:
            if confirmacao == "S":
                exclui = cur.execute(
                    """
                    DELETE FROM LIVRO WHERE ID_livro = :id_livro
                    """, {"id_livro": id_livro})
                if exclui:
                    print("Livro excluido com sucesso.")
            elif confirmacao == "N":
                print("Operação cancelada.")
        raise KeyError("Livro não cadastrado.")
    except KeyError as e:
        print("Erro ao excluir livro: ", e)