import json
import oracledb
import sqlalchemy


dsn_str = oracledb.makedsn("oracle.fiap.com.br", 1521, "ORCL")
connection = oracledb.connect(user='rm556857', password='260105', dsn=dsn_str)