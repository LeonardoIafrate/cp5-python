import json
import oracledb
import sqlalchemy
from connection import connection

con = connection
cur = con.cursor()


def cadastra_genero():
    try:
        genero_livro = input("Digite o gênero que deseja cadastrar: ")
        cur.execute(
        """
        INSERT INTO GENERO(Genero)
        VALUES(:genero)
        """, genero = genero_livro
        )
        con.commit()
    except oracledb.IntegrityError:
        print("Genero já cadastrado!")


def altera_genero():
    try:
        genero = input("Digite o gênero: ")
        genero_alterado = input("Digite o gênero com a alteração: ")
        cur.execute(
        """
        UPDATE GENERO SET Genero = :genero_alterado WHERE Genero = :genero
        """, {"genero": genero, "genero_alterado": genero_alterado}
        )
        if cur.rowcount == 0:
            raise KeyError(f"O gênero '{genero}' não está cadastrado na tabela.")
        con.commit()
        print(f"Gênero '{genero_alterado}' alterado com sucesso!")
    except KeyError as ke:
        print(f"Erro ao alterar gênero: ", ke)



def exclui_genero():
    try:
        genero = input("Digite o gênero que deseja excluir: ")
        confirmacao = input(f"Tem certeza que deseja excluir o genero {genero}? (S/N)").upper
        cur.execute("SELECT GENERO FROM GENERO WHERE Genero = :genero", {"genero": genero})
        listar_genero = cur.fetchone()
        if listar_genero:
            if confirmacao == "S":
                cur.execute(
                """
                DELETE FROM GENERO WHERE Genero = :genero
                """, {"genero": genero})
                con.commit()
            elif confirmacao == "N":
                print("Operação cancelada!")
        raise KeyError("Gênero não cadastrado")
    except KeyError as e:
        print("Erro ao excluir o gênero: ", e)