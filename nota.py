from psycopg import errors
from banco import conectar

# Metodos extras
def consultar_ids(conn):
    try:
        with conn.cursor() as cur:
            # Query para retornar todos os IDs possiveis
            cur.execute(
                """
                SELECT
                    a.nome,
                    a.id
                FROM
                    aluno a;
                """
            )
            ids = cur.fetchall()

            print(f"-- ALUNOS REGISTRADOS --")
            if not ids:
                print("* Nenhum aluno cadastrado *")
                return

            for al_id in ids:
                print(f"Nome: {al_id[0]:<25} ID: {al_id[1]}")
                
    finally:
        cur.close()

    while True:
        try:
            aluno_id = int(input("\n- Insira um ID para pesquisa: "))

            if aluno_id < 1:
                print("\n* O ID inserido nao pode ser negativo *")
                continue
            
            return aluno_id
        
        except ValueError:
            return 0

def consultar_avaliacoes(conn, aluno_id):
    try:
        with conn.cursor() as cur:
            # Query para obter todas as avaliacoes de um aluno
            cur.execute(
                """
                SELECT
                    n.nota,
                    n.descricao
                FROM
                    nota n
                WHERE
                    n.aluno_id = %s;
                """,
                (aluno_id,)
            )
            avaliacoes = cur.fetchall()
            return avaliacoes
        
    finally:
        cur.close()


def cadastrar_nota():
    conn = conectar()
    if not conn:
        return

    # Adquire os valores para insercao
    print("\n-- CADASTRO DE NOTA --")
    aluno_id = input("- Insira o ID do aluno: ")
    descricao = input("- Insira a DESCRICAO da avaliacao: ")
    dt_avaliacao = input("- Insira a DATA da avaliacao(YYYY-MM-DD): ")
    while True:
        try:
            nota = float(input("- Insira a NOTA da avaliacao: "))

            if nota < 0 or nota > 10:
                print("\n* A nota deve estar entre \'0\' e \'10\'. Insira novamente *")
                continue

            break

        except ValueError:
            print("\n* Apenas valores numericos sao aceitos *")

    # Impede que informacoes "VAZIAS" sejam inseridas
    if not all([aluno_id, descricao, dt_avaliacao]):
        print("\n* Impossivel adicionar com INFORMACOES vazias *")
        conn.close()
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO
                    nota(aluno_id, descricao, nota, data_avaliacao)
                VALUES
                    (%s, %s, %s, %s)
                RETURNING
                    id;
                """,
                (aluno_id, descricao, nota, dt_avaliacao)
            )
            # Confirma a gravacao
            conn.commit()

            # Captura do retorno
            registro_inserido = cur.fetchone()

            if registro_inserido:
                print("\n-- CADASTRO CONCLUIDO --")
                print(f"* Nota cadastrada com ID: {registro_inserido[0]} *")
            else:
                print("\n* FALHA NO CADASTRO *")

    except errors.InvalidDatetimeFormat as e:
        print("\n[ERROR] Formato de hora errada. Impossivel adicionar ao banco")
        print(f"[DETAILS] {e}")

    except errors.ForeignKeyViolation as e:
        print("\n[ERROR] Impossivel inserir valores ao banco de dados")
        print(f"[DETAILS] {e}")

    finally:
        conn.close()

def consultar_boletim():
    conn = conectar()
    if not conn:
        return

    # Input de ID para pesquisa
    aluno_id = consultar_ids(conn)

    # Avaliacoes por ID
    avaliacoes = consultar_avaliacoes(conn, aluno_id)
    if not avaliacoes:
        print("* Nenhuma avaliacao cadastrada para este aluno *")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    a.nome,
                    ROUND(AVG(n.nota), 2) as media,
                    CASE
                        WHEN AVG(n.nota) >= 7 THEN 'Aprovado'
                        WHEN AVG(n.nota) >= 5 THEN 'Recuperacao'
                        ELSE 'Reprovado'
                    END as status
                FROM
                    aluno a
                JOIN
                    nota n
                    ON a.id = n.aluno_id
                WHERE
                    a.id = %s
                GROUP BY
                    a.nome;
                """,
                (aluno_id,)
            )
            boletim = cur.fetchone()

            print("\n-- BOLETIM --")
            if not boletim:
                print("* Este ID nao possui nenhuma avaliacao relacionada *")
                return

            print(f"- Nome: {boletim[0]}")
            print("- Avaliacoes:")
            for a in avaliacoes:
                print(f"  {a[1]} - Nota: {a[0]}")
            print(f"- Nota media: {boletim[1]}")
            print(f"- Status de aprovacao: {boletim[2]}")
        
    finally:
        conn.close()

def ranking_turma():
    conn = conectar()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    a.nome,
                    ROUND(AVG(n.nota), 2) AS media
                FROM 
                    aluno a
                JOIN
                    nota n
                    ON a.id = n.aluno_id
                GROUP BY
                    a.nome
                ORDER BY
                    media DESC;
                """
            )
            ranking = cur.fetchall()

            print("\n-- RANKING DA TURMA --")
            if not ranking:
                print("* Nenhuma nota cadastrada *")

            for i, al in enumerate(ranking, start=1): # Enumerate entrega indice e os itens da lista ao mesmo tempo
                print(f"{i}- {al[0]:<25} Media: {al[1]}") # "RESERVA" 25 espacos para o nome

    finally:
        conn.close()
