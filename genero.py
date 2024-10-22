import json
import oracledb
import sqlalchemy
from connection import connection

con = connection
cur = con.cursor()

def cadastra_genero():
    genero_livro = input("Digite o gênero que deseja cadastrar: ")
    cur.execute(
    """
    INSERT INTO GENERO(Genero)
    VALUES(:genero)
    """, genero = genero_livro
    )
    con.commit()

def altera_genero():
    id_genero = input("Digite o id do gênero que deseja alterar: ")
    genero = input("Digite o gênero: ")
    cur.execute(
    """
    UPDATE GENERO SET Genero = :genero WHERE ID_genero = :id_genero
    """, {"genero": genero, "id_genero": id_genero}
    )
    con.commit()

def exclui_genero():
    id_genero = input("Digite o id do gênero que deseja excluir: ")
    genero = cur.execute("SELECT GENERO FROM GENERO WHERE ID_genero = :id_genero", {"id_genero":id_genero})
    confirmacao = input(f"Tem certeza que deseja excluir o genero {genero}? (S/N)").upper
    if confirmacao == "S":
        cur.execute(
        """
        DELETE FROM GENERO WHERE ID_genero = :id_genero
        """, {"id_genero": id_genero})
        con.commit()
    elif confirmacao == "N":
        print("Operação cancelada!")