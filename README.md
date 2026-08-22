# SISTEMA DE GESTÃO APRIMORADA DE ALUNOS

### Objetivo
Sistema evoluído para realizar o cadastro e gerenciamento de alunos e notas, garantindo a persistência robusta dos dados por meio de um banco de dados relacional PostgreSQL. 
O projeto foi estruturado para melhor organização do código em módulos separados, com foco em segurança contra SQL Injection, validações em camadas e uso de recursos nativos avançados da linguagem Python.

### Funcionalidades
*   **Persistência Relacional** - Salvamento e gerenciamento estruturado das informações de alunos e avaliações utilizando PostgreSQL;
*   **Gestão Completa de Alunos** - Cadastro, consulta flexível por parte do nome (com uso do operador `ILIKE`), alteração e listagem geral de registros;
*   **Controle de Notas e Boletins** - Cadastro de avaliações vinculadas por chave estrangeira, emissão de boletins individuais com cálculo automático de média e status acadêmico, além de ranking geral da turma ordenado por desempenho;
*   **Tratamento de Exceções do SGBD** - Captura inteligente de erros do banco de dados (violações de chave única, formato inválido de data, erros de chave estrangeira e indisponibilidade de conexão) sem encerrar a aplicação de forma inesperada;
*   **Validação de Entrada** - Bloqueio preventivo de dados vazios no lado da aplicação e restrições de integridade no banco de dados.

### Tecnologias Utilizadas
*   **Linguagem**: Python (versão 3.10 ou superior, utilizando recursos como `match...case`);
*   **Banco de Dados**: [PostgreSQL](https://www.postgresql.org/docs/) (SGBD relacional);
*   **Biblioteca de Integração**: [Psycopg 3](https://www.psycopg.org/psycopg3/docs/) (para comunicação Python-PostgreSQL);
*   **Controle de Versões**: Git e GitHub.

### Estrutura do Banco de Dados (DDL)
O sistema utiliza duas tabelas principais integradas por chave estrangeira:
*   `aluno`: Armazena dados cadastrais (`id`, `nome`, `status`, `data_nascimento`, `email`, `telefone`, `cpf` e `criado_em`), com restrições de unicidade (`UNIQUE`) para CPF, e-mail e telefone.
*   `nota`: Armazena as avaliações (`id`, `aluno_id`, `descricao`, `nota`, `data_avaliacao` e `criado_em`), contendo uma regra de verificação (`CHECK`) para garantir que as notas estejam estritamente entre 0 e 10.

### Como Executar?

**Pré-Requisitos:**
Verifique se os seguintes programas estão instalados na sua máquina:
* [Git](https://git-scm.com/downloads)
* [Python 3.10 ou superior](https://www.python.org/downloads/)
* [PostgreSQL](https://www.postgresql.org/downloads/) configurado e rodando localmente

**1 - Clonar o repositório**
Abra o terminal e rode o comando abaixo para baixar o código:

```bash
git clone https://github.com/HenriqueEnglert/gestao-alunos-python
```

**2 - Instalação de dependências**
Abra o terminal dentro da pasta raiz do projeto e instale a biblioteca do PostgreSQL rodando o comando:

```bash
pip install -r requirements.txt
```

**3 - Configuração do Banco de Dados**
Certifique-se de criar um banco de dados chamado `gestao_alunos` no seu PostgreSQL e executar os scripts DDL das tabelas `aluno` e `nota`. Se necessário, ajuste os parâmetros de conexão no arquivo `banco.py` (host, port, dbname, user, password).

**4 - Executando o sistema**
No terminal integrado dentro da pasta raiz do projeto, execute o arquivo principal:

```bash
python main.py
```

### Conceitos Utilizados
*   **Modularização**: Divisão de responsabilidades em arquivos separados (`main.py`, `banco.py`, `aluno.py`, `nota.py`);
*   **Segurança de Dados**: Utilização de *Query Parameterization* nas queries SQL para prevenir ataques de *SQL Injection*;
*   **Delegação de Processamento ao SGBD**: Uso de funções agregadas (`AVG`, `ROUND`), agrupamentos (`GROUP BY`), ordenações (`ORDER BY`) e condicionais nativas (`CASE WHEN`) diretamente no PostgreSQL;
*   **Estruturas de Controle Avançadas**: Uso de `match...case` para o roteamento do menu principal;
*   **Tratamento de Erros em Camadas**: Captura de exceções específicas do driver de conexão (`OperationalError`, `UniqueViolation`, `InvalidDatetimeFormat`, `ForeignKeyViolation`).

### Dificuldades Enfrentadas
*   **Inserção de Strings Vazias no Banco**: Durante a validação inicial dos cadastros, percebeu-se que o usuário conseguia enviar campos preenchidos apenas com espaços vazios ou nulos que burlavam parcialmente o fluxo lógico antes de atingirem as restrições rígidas do banco, exigindo uma validação prévia robusta no lado do Python.
*   **Gerenciamento de Múltiplos Blocos de Condição**: O código original exigia diversos blocos `if` encadeados para verificar individualmente se cada variável de entrada continha dados preenchidos, gerando muita poluição visual e repetição de código (`boilerplate`).

### Soluções Adotadas
*   **Validação Prévia com o Método `all()`**: Implementou-se o método nativo `all()` do Python para inspecionar a lista de variáveis de entrada de uma só vez logo antes de executar a query de inserção no banco de dados, interrompendo o fluxo imediatamente caso qualquer campo estivesse vazio.
*   **Descoberta Orientada por IA**: A descoberta do método `all()` para simplificar múltiplos blocos `if` ocorreu ao enviar um prompt ao agente de IA Gemini, questionando se havia alguma maneira elegante e simplificada de encerrar o método caso alguma informação estivesse vazia, otimizando drasticamente a legibilidade do código.
*   **Parametrização de Consultas**: Adoção estrita de parâmetros (%s) nas execuções do cursor do Psycopg 3 para mitigar vulnerabilidades e garantir a integridade dos dados enviados ao PostgreSQL.