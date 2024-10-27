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

#Altera gênero aqui
#->
###

#Exclui genero aqui 
#->
#