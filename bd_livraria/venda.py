import json
import oracledb
from datetime import datetime
from fastapi import HTTPException
from bd_livraria.connection import *

def cadastra_venda_e_livros(nome_cliente: str, livros: list):
    data_venda = datetime.now().strftime("%d-%m-%Y")
    id_venda = cur.var(int)

    try:
        # Cadastra a venda
        cur.execute(
            """
            INSERT INTO VENDA(DATA_VENDA, NOME_CLIENTE)
            VALUES (TO_DATE(:DATA_VENDA, 'DD-MM-YYYY'), :NOME_CLIENTE)
            RETURNING ID_VENDA INTO :id_venda
            """, 
            {"DATA_VENDA": data_venda, "NOME_CLIENTE": nome_cliente, "id_venda": id_venda}
        )
        id_venda = id_venda.getvalue()
        con.commit()

        # Cadastra os livros da venda
        for livro in livros:
            id_livro = livro['id_livro']
            quantidade = livro['quantidade']
            cadastra_venda_livro(id_venda, id_livro, quantidade)

        return {"Message": f"Venda cadastrada com sucesso, ID da venda: {id_venda}, data venda: {data_venda}"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar venda: {str(e)}")


def cadastra_venda_livro(id_venda: int, id_livro: int, qnt: int):
    cur.execute(
        """
        INSERT INTO VENDA_LIVROS(ID_VENDA, ID_LIVRO, QUANTIDADE)
        VALUES (:ID_VENDA, :ID_LIVRO, :QUANTIDADE)
        """, 
        {"ID_VENDA": id_venda, "ID_LIVRO": id_livro, "QUANTIDADE": qnt}
    )
    con.commit()


# def cadastra_venda(nome_cliente: str, num_livros: int):
    

#     id_livro = int 
#     qnt = int
#     data_venda = datetime.now().strftime("%d-%m-%Y")
#     id_venda = cur.var(int)

#     try:
#         cur.execute(
#         """
#         INSERT INTO VENDA(DATA_VENDA, NOME_CLIENTE)
#         VALUES (TO_DATE(:DATA_VENDA, 'DD-MM-YYYY'), :NOME_CLIENTE)
#         RETURNING ID_VENDA INTO :id_venda
#         """, {"DATA_VENDA": data_venda, "NOME_CLIENTE": nome_cliente, "id_venda": id_venda}
#         )
#         id_venda = id_venda.getvalue()
#         con.commit()
#         for livros in range(num_livros):
#             cur.execute(
#             """
#             INSERT INTO VENDA_LIVROS(ID_VENDA, ID_LIVRO, QUANTIDADE)
#             VALUES (:id_venda, :id_livro, :qnt)
#             """, {"id_venda": id_venda, "id_livro": id_livro, "qnt": qnt})
#         # return{"Message": f"Venda cadastrado com sucesso, ID da venda: {id_venda}, data venda: {data_venda}"}
#         return{"Livros": livros}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=f"Erro ao cadastrar venda {str(e)}")


# def cadastra_venda_livro(id_venda: int, id_livro: int, qnt: int):
#     cur.execute(
#     """
#     INSERT INTO VENDA_LIVROS(ID_VENDA, ID_LIVRO, QUANTIDADE)
#     VALUES (:ID_VENDA, :ID_LIVRO, :QUANTIDADE)
#     """, {"ID_VENDA": id_venda, "ID_LIVRO": id_livro, "QUANTIDADE": qnt}
#     )
#     con.commit()
#     return{"Message": "Venda finalizada com sucesso!"}

def altera_venda_livro(id_venda: int, id_livro: int, quantidade: int):
    cur.execute("SELECT * FROM VENDA_LIVROS WHERE ID_VENDA = :id_venda", {"id_venda": id_venda})
    venda = cur.fetchone()
    
    if venda is None:
        raise HTTPException(status_code=404, detail="venda livro não encontrado")
    
    try:
        cur.execute(
        """
        UPDATE VENDA_LIVROS SET id_venda = :id_venda, id_livro = :id_livro, quantidade = :quantidade WHERE ID_VENDA = :id_venda
        """, {"id_venda": id_venda, "id_livro": id_livro, "quantidade": quantidade}
        )
        con.commit()
        return {"Message": "Venda livro alterada com sucesso"}
    except Exception as e:
        return {"Erro": f"Um erro inesperado aconteceu, {str(e)}"}
    
    
def altera_venda(id_venda: int, data_venda: int, nome_cliente: str):
    cur.execute("SELECT * FROM VENDA WHERE ID_VENDA = :id_venda", {"id_venda": id_venda})
    venda = cur.fetchone()
    
    if venda is None:
        raise HTTPException(status_code=404, detail="venda não encontrado")
    
    try:
        cur.execute(
        """
        UPDATE VENDA SET data_venda = :data_venda, nome_cliente = :nome_cliente WHERE ID_VENDA = :id_venda
        """, {"id_venda": id_venda, "nome_cliente": nome_cliente, "data_venda": data_venda}
        )
        con.commit()
        return {"Message": "Venda alterada com sucesso"}
    except Exception as e:
        return {"Erro": f"Um erro inesperado aconteceu, {str(e)}"}

def excluir_venda():
    try:
        Id_venda = input("Digite o id da venda que deseja excluir: ")
        confirmacao = input(f"Tem certeza que deseja excluir a venda {Id_venda}? (S/N)").upper
        cur.execute("SELECT ID_VENDA FROM VENDA WHERE ID_VENDA = :ID_VENDA", {"ID_VENDA": Id_venda})
        listar_venda = cur.fetchone()
        if listar_venda:
            if confirmacao == "S":
                cur.execute(
                """
                DELETE FROM VENDA WHERE ID_VENDA = :id_venda
                """, {"id_venda": Id_venda})
                cur.execute(
                """
                DELETE FROM VENDA_LIVRO WHERE ID_VENDA = :id_venda
                """, {"id_venda": Id_venda})
                con.commit()
            elif confirmacao == "N":
                print("Operação cancelada!")
        raise KeyError("venda não cadastrada")
    except KeyError as e:
        print("Erro ao excluir venda: ", e)


def relatorio_venda(): 
    try:
        id_venda = input("Digite o ID da venda para gerar o relatório: ")
        
        cur.execute('''
        SELECT 
            v.ID_VENDA, 
            v.NOME_CLIENTE, 
            TO_CHAR(v.DATA_VENDA, 'YYYY-MM-DD') AS DATA_VENDA, 
            l.ID_LIVRO, 
            l.TITULO,
            vl.QUANTIDADE,
            l.PRECO * vl.QUANTIDADE AS VALOR_TOTAL
        FROM 
            Venda v
        JOIN 
            Venda_Livros vl ON v.ID_VENDA = vl.ID_VENDA
        JOIN 
            Livro l ON vl.ID_LIVRO = l.ID_LIVRO
        WHERE 
            v.ID_VENDA = :id_venda
        ''', {"id_venda": id_venda})
    except KeyError as e:
        print("Erro ao exibir relatorio de venda: ", e)
