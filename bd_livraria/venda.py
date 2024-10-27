import json
import oracledb
from datetime import datetime
from fastapi import HTTPException
from bd_livraria.connection import *
    
    
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

def excluir_venda(id_venda: int):
    try:
        cur.execute("SELECT ID_VENDA FROM VENDA WHERE ID_VENDA = :ID_VENDA", {"ID_VENDA": id_venda})
        listar_venda = cur.fetchone()
        if listar_venda:
            cur.execute(
            """
            DELETE FROM VENDA_LIVROS WHERE ID_VENDA = :id_venda
            """, {"id_venda": id_venda})
            cur.execute(
            """
            DELETE FROM VENDA WHERE ID_VENDA = :id_venda
            """, {"id_venda": id_venda})
            con.commit()
            return {"Message": "Venda excluída com sucesso"}
        else:
            return{"Error": "Venda não cadastrada"}
    except oracledb.IntegrityError as e:
            return {"Error": f"Erro ao excluir venda: {str(e)}"}


def relatorio_venda(id_venda: int): 
    try:
        cur.execute("""
        SELECT 
            v.ID_VENDA, 
            v.NOME_CLIENTE, 
            TO_CHAR(v.DATA_VENDA, 'DD-MM-YYYY') AS DATA_VENDA, 
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
        """, {"id_venda": id_venda})
        items = cur.fetchall()
        
        
        relatorio = []
        valor_total = 0
        for item in items:
            relatorio_dict = {
                "ID da venda ": item[0],
                "Nome do cliete": item[1],
                "Data da venda": item[2],
                "ID do livro": item[3],
                "Título do livro": item[4],
                "Quantidade vendida": item[5],
                "Valor total do livro na venda": f"R${item[6]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')}
            relatorio.append(relatorio_dict)
            valor_total += item[6]
        return {
            "relatorio": relatorio,
            "Valor total da venda": f"R${valor_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        }


    except KeyError as e:
        print("Erro ao exibir relatorio de venda: ", e)
