import sys
from banco import conectar
from aluno import cadastrar_aluno, pesquisar_aluno, listar_alunos
from nota import cadastrar_nota, consultar_boletim, ranking_turma

def exibir_menu():
    print("\n-- MENU INICIAL --")
    print("1- Cadastrar Aluno")
    print("2- Pesquisar Aluno")
    print("3- Listar Alunos")
    print("4- Cadastar nota")
    print("5- Consultar Boletim")
    print("6- Ranking da turma")
    print("7- SAIR")

# Apagar em algum momento
def testar_conexao():
    conn = conectar()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_date;")
            data = cur.fetchone()[0]
            print("\nCONEXAO REALIZADA COM SUCESSO")
            print(f"\nDATA DO SERVIDOR POSTGRES: {data}")

        conn.close()
        return True

    return False

def main():
    slct = None

    while slct != 7:
        exibir_menu()

        try: 
            slct = int(input("Escolha uma opcao: "))

            if slct < 1 or slct > 7:
                print("Input Invalido - Escolha uma opcao valida (1 a 6)")
                continue

        except ValueError:
            print("[ERROR]: Apenas numeros sao permitidos - Escolha uma opcao valida (1 a 6)")
            continue

        match slct:
            case 1:
                cadastrar_aluno()
            case 2:
                pesquisar_aluno()
            case 3:
                listar_alunos()
            case 4:
                cadastrar_nota()
            case 5:
                consultar_boletim()
            case 6:
                ranking_turma()
            case 7:
                print("\nEncerrando o sistema...")
                sys.exit(1)
        

# ================================================================================================= #
    print("\nINICIANDO O SISTEMA")
    if not testar_conexao():
        print("\nENCERRANDO PROGRAMA DEVIDO AO ERRO DE CONEXAO")
        sys.exit(1)

    listar_alunos()


if __name__ == "__main__":
    main()