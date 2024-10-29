import oracledb
from bd_livraria.autor import *


def cadastrar_livro(titulo_livro: str, qnt_pag: int, id_autor: int, preco: float, genero: str):
    
    titulo_livro = titulo_livro.upper()
    genero = genero.upper()

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


def deleta_livro(id_livro: int):
    cur.execute("SELECT Titulo FROM LIVRO WHERE ID_livro = :id_livro", {"id_livro": id_livro})
    livro_existe = cur.fetchone()
    
    if livro_existe is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    try:
        cur.execute(
        """
        DELETE FROM LIVRO WHERE ID_livro = :id_livro
        """, {"id_livro": id_livro})
        con.commit()
        return {"Message": "Livro excluído com sucesso"}
    except oracledb.IntegrityError as e:
        return {"Message": f"Livro não cadastrado{str(e)}"}