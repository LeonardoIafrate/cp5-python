import json
import oracledb
import sqlalchemy
from fastapi import HTTPException
from bd_livraria.connection import *

con = connection
cur = con.cursor()


def cadastra_genero(genero_livro: str):
    try:
        genero_livro = genero_livro.upper()
        cur.execute(
        """
        INSERT INTO GENERO(Genero)
        VALUES(:genero)
        """, genero = genero_livro
        )
        con.commit()
        return {"Message": "Genero cadastrado com sucesso"}
    except oracledb.IntegrityError:
        return {"Error": "Genero já cadastrado!"}

def altera_genero(genero_livro: str, novo_genero: str):
    genero_livro = genero_livro.upper()
    cur.execute("SELECT * FROM GENERO WHERE GENERO = :genero_livro", {"genero_livro": genero_livro})
    genero_existe = cur.fetchone()

    if genero_existe is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    try:
        novo_genero = novo_genero.upper()
        cur.execute(
        """
        UPDATE GENERO SET Genero = :genero_alterado WHERE Genero = :genero
        """, {"genero": genero_livro, "genero_alterado": novo_genero}
        )
        con.commit()
        return {"Message": "Genero alterado com sucesso"}

    except oracledb.IntegrityError as e:
        return {"Error": f"Erro ao alterar o livro {str(e)}"}
    
    
def exclui_genero(genero_livro: str):
    genero_livro = genero_livro.upper()
    cur.execute("SELECT GENERO FROM GENERO WHERE Genero = :genero", {"genero": genero_livro})
    genero_existe = cur.fetchone()
    
    if genero_existe is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    try:
        cur.execute(
        """
        DELETE FROM GENERO WHERE Genero = :genero
        """, {"genero": genero_livro})
        con.commit()
        return{"Message": "Livro excluido com sucesso"}

    except oracledb.IntegrityError as e:
        return {"Error": f"Erro ao alterar o livro {str(e)}"}
    
