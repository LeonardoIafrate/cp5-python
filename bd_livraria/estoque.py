import json
import oracledb
import sqlalchemy
from bd_livraria.connection import *

con = connection

def total_estoque():
    cur.execute("SELECT SUM(Qnt_estoque) FROM ESTOQUE")
    total = cur.fetchone()[0]
    return total if total is not None else 0


def adiciona_quantidade(id_livro, qnt):
    cur.execute(
        """
        UPDATE ESTOQUE SET Qnt_estoque = Qnt_estoque + :add_qnt WHERE ID_livro = :id_livro 
        """, {"add_qnt": qnt, "id_livro": id_livro}
    )
    if total_estoque() > 25000:
        raise ValueError("A capacidade máxima do estoque é de 25000")
    else:
        con.commit()
        print("Quantidade adicionada com sucesso!")

def remove_quantidade(id_livro,qnt):
    try:
        cur.execute(
            """
            UPDATE ESTOQUE SET Qnt_estoque = (Qnt_estoque - :qnt) WHERE ID_livro = :id_livro 
            """, {"qnt": qnt, "id_livro": id_livro}
        )
        con.commit()
        print("Quantidade removida com sucesso!")
    except oracledb.IntegrityError as e:
        print("Erro ao remover estoque: um livro não pode ter uma quantidade negativa")

def adiciona_estoque():
    try:
        id_livro = input("Digite o ID do livro a ser adicionado: ")
        
        cur.execute("SELECT ID_livro FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
        livro_cadastrado = cur.fetchone()

        if livro_cadastrado:
            cur.execute("SELECT Qnt_estoque FROM ESTOQUE WHERE ID_livro = :id_livro", {"id_livro": id_livro})
            livro_no_estoque = cur.fetchone()
            if livro_no_estoque:
                qnt = input("Digite a quantidade a ser adicionada ao estoque: ")
                adiciona_quantidade(id_livro, qnt)
            else:
                cur.execute(
                """
                INSERT INTO ESTOQUE(ID_livro, Qnt_estoque)
                VALUES(:id_livro, 0)
                """, {"id_livro": id_livro}
                )
                con.commit()
                qnt = input("Digite a quantidade a ser adicionada ao estoque: ")
                adiciona_quantidade(id_livro, qnt)
        else:
            raise KeyError("Nenhum livro possui esse ID")
    except KeyError as e:
        print("Erro ao adicionar estoque: ", e)


def remove_estoque():
    try:
        id_livro = input("Digite o ID do livro a ser removido: ")
        
        cur.execute("SELECT ID_livro FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
        livro_cadastrado = cur.fetchone()
        
        if livro_cadastrado:
            qnt = input("Digite a quantidade a ser removida do estoque: ")
            remove_quantidade(id_livro,qnt)
        else:
            raise KeyError("Nenhum livro possui esse ID")
    except KeyError as e:
        print("Erro ao remover estoque: ", e)
