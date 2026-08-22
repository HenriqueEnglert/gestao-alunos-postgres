import psycopg
from psycopg import OperationalError

CONFIG = {
    "host" : "127.0.0.1",
    "port" : "5432",
    "dbname" : "gestao_alunos",
    "user" : "postgres",
    "password" : "postgres"
}

def conectar():
    try:
        conn = psycopg.connect(**CONFIG)

        return conn

    except OperationalError as e:
        print("\n[ERROR] Erro ao conectar ao banco de dados")
        print(f"[DETAILS] {e}")

        return None