from psycopg import errors
from banco import conectar

def cadastrar_aluno():
    # Realiza a conexao com o DB
    conn = conectar()
    if not conn:
        return

    # Adquire os valores para insercao
    print("\n-- CADASTRO DE ALUNO --")
    nome = input("- Insira o NOME do aluno: ")
    dt_nasc = input("- Insira a DATA DE NASCIMENTO do aluno(YYYY-MM-DD): ")
    email = input("- Insira o EMAIL do aluno: ")
    telefone = input("- Insira o numero de TELEFONE do aluno((DDD)XXXXX-XXXX): ")
    cpf = input("- Insira o CPF do aluno(XXXXXXXXXXX): ")

    # Impede que informacoes "VAZIAS" sejam inseridas
    if not all([nome, dt_nasc, email, telefone, cpf]):
        print("\n* Impossivel adicionar com INFORMACOES vazias *")
        conn.close()
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO
                    aluno(nome, status, data_nascimento, email, telefone, cpf)
                VALUES
                    (%s, 'Ativo', %s, %s, %s, %s)
                RETURNING
                    id;
                """,
                (nome, dt_nasc, email, telefone, cpf)
            )
            # Confirma a gravacao
            conn.commit()

            # Captura do retorno
            registro_inserido = cur.fetchone()

            if registro_inserido:
                print("\n-- CADASTRO CONCLUIDO --")
                print(f"* Aluno cadastrado com ID: {registro_inserido[0]} *")
            else:
                print("\n* FALHA NO CADASTRO *")

    except errors.InvalidDatetimeFormat as e:
        print("\n[ERROR] Formato de hora errada. Impossivel adicionar ao banco")
        print(f"[DETAILS] {e}")

    except errors.UniqueViolation as e:
        print("\n[ERROR] Impossivel inserir valores ao banco de dados")
        print(f"[DETAILS] {e}")

    finally:
        conn.close()

def pesquisar_aluno():
    conn = conectar()
    if not conn:
        return

    nome = input("\n- Insira parte do NOME para consulta: ")

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    a.id,
                    a.nome
                FROM
                    aluno AS a
                WHERE
                    a.nome ILIKE %s;
                """,
                (f"%{nome}%",)
            )
            alunos = cur.fetchall()

            print("\n-- RESULTADOS DA PESQUISA --")
            if not alunos:
                print("* Nenhum resultado correspondente *")

            for al in alunos:
                print("* ===== *")
                print(f"ID: {al[0]}")
                print(f"NOME: {al[1]}")
                print("* ===== *\n")

    finally:
        conn.close()

def listar_alunos():
    conn = conectar()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
            """
            SELECT id,
            nome,
            status,
            data_nascimento,
            email,
            telefone,
            cpf,
            criado_em
            FROM aluno
            ORDER BY id;
            """)
            aluno = cur.fetchall()

            print("\n-- ALUNOS CADASTRADOS --\n")
            if not aluno:
                print("* Nenhum aluno listado *")

            for al in aluno:
                print("* ===== *")
                print(f"ID: {al[0]}")
                print(f"NOME: {al[1]}")
                print(f"STATUS: {al[2]}")
                print(f"DATA_NASCIMENTO: {al[3]}")
                print(f"EMAIL: {al[4]}")
                print(f"TELEFONE: {al[5]}")
                print(f"CPF: {al[6]}")
                print(f"CRIADO_EM: {al[7]}")
                print("* ===== *\n")

    finally:
        conn.close()
