import re

__all__ = [
    "cadastrar_aluno",
    "validar_login",
    "consultar_aluno",
    "atualizar_aluno",
    "remover_aluno",
    "aluno_existe",
    "aluno_esta_ativo",
    "aluno_pode_pegar_emprestimo",
    "incrementar_emprestimos_ativos",
    "decrementar_emprestimos_ativos",
    "registrar_atraso_aluno",
    "consultar_email_aluno",
    "listar_alunos",
]

# Códigos de retorno
SUCESSO               = 0
ERRO_ID_INEXISTENTE   = 1
ERRO_ID_REPETIDO      = 2
ERRO_DADOS_INVALIDOS  = 3
ERRO_OPERACAO_INVALIDA= 4
ERRO_LIMITE_ATINGIDO  = 5
ERRO_INDISPONIVEL     = 6
ERRO_INATIVO          = 7
ERRO_ATRASO           = 8
ERRO_LISTA_VAZIA      = 9

MAX_EMPRESTIMOS = 3

# Estrutura de dados interna — lista de dicionários
alunos = []

# ---------------------------------------------------------------------------
# Funções auxiliares internas (não exportadas)
# ---------------------------------------------------------------------------

def _email_valido(email):
    """Verifica formato básico de e-mail."""
    padrao = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return re.match(padrao, email) is not None

def _buscar_aluno(id_aluno):
    """Retorna o dicionário do aluno ou None."""
    for aluno in alunos:
        if aluno['id_aluno'] == id_aluno:
            return aluno
    return None

def _matricula_em_uso(matricula, ignorar_id=None):
    """Verifica se a matrícula já existe, ignorando um id específico."""
    for aluno in alunos:
        if aluno['matricula'] == matricula and aluno['id_aluno'] != ignorar_id:
            return True
    return False

def _email_em_uso(email, ignorar_id=None):
    """Verifica se o e-mail já existe, ignorando um id específico."""
    for aluno in alunos:
        if aluno['email'] == email and aluno['id_aluno'] != ignorar_id:
            return True
    return False

# ---------------------------------------------------------------------------
# Interface pública
# ---------------------------------------------------------------------------

def cadastrar_aluno(id_aluno, nome, data_nascimento, matricula, curso, email, senha):
    """
    Cadastra um novo aluno no sistema.
    Retorna (codigo, None).
    """
    # Validação de dados obrigatórios
    if (not id_aluno or not str(id_aluno).strip()
            or not nome or not str(nome).strip()
            or not data_nascimento or not str(data_nascimento).strip()
            or not matricula or not str(matricula).strip()
            or not curso or not str(curso).strip()
            or not email or not str(email).strip()
            or not senha or not str(senha).strip()):
        return (ERRO_DADOS_INVALIDOS, None)

    matricula = str(matricula).strip()
    email     = str(email).strip()
    senha     = str(senha).strip()
    nome      = str(nome).strip()
    curso     = str(curso).strip()

    if not _email_valido(email):
        return (ERRO_DADOS_INVALIDOS, None)

    # Unicidade: id, matrícula e e-mail
    if _buscar_aluno(id_aluno) is not None:
        return (ERRO_ID_REPETIDO, None)
    if _matricula_em_uso(matricula):
        return (ERRO_ID_REPETIDO, None)
    if _email_em_uso(email):
        return (ERRO_ID_REPETIDO, None)

    novo_aluno = {
        'id_aluno'                  : id_aluno,
        'nome'                      : nome,
        'data_nascimento'           : str(data_nascimento).strip(),
        'matricula'                 : matricula,
        'curso'                     : curso,
        'email'                     : email,
        'senha'                     : senha,
        'qtd_emprestimos_ativos'    : 0,
        'max_emprestimos_ativos'    : MAX_EMPRESTIMOS,
        'ativo'                     : True,
    }
    alunos.append(novo_aluno)
    return (SUCESSO, None)


def validar_login(matricula, senha):
    """
    Valida login por matrícula e senha.
    Retorna (codigo, id_aluno) em caso de sucesso.
    """
    if not matricula or not str(matricula).strip() or not senha or not str(senha).strip():
        return (ERRO_DADOS_INVALIDOS, None)

    matricula = str(matricula).strip()
    senha     = str(senha).strip()

    for aluno in alunos:
        if aluno['matricula'] == matricula:
            if aluno['senha'] == senha:
                return (SUCESSO, aluno['id_aluno'])
            else:
                return (ERRO_OPERACAO_INVALIDA, None)

    return (ERRO_ID_INEXISTENTE, None)


def consultar_aluno(id_aluno):
    """
    Consulta os dados completos de um aluno.
    Retorna (codigo, aluno) ou (codigo, None).
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, None)
    return (SUCESSO, dict(aluno))


def atualizar_aluno(id_aluno, nome, data_nascimento, matricula, curso, email):
    """
    Atualiza dados cadastrais de um aluno existente.
    Retorna (codigo, None).
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, None)

    # Validação de dados
    if (not nome or not str(nome).strip()
            or not data_nascimento or not str(data_nascimento).strip()
            or not matricula or not str(matricula).strip()
            or not curso or not str(curso).strip()
            or not email or not str(email).strip()):
        return (ERRO_DADOS_INVALIDOS, None)

    matricula = str(matricula).strip()
    email     = str(email).strip()

    if not _email_valido(email):
        return (ERRO_DADOS_INVALIDOS, None)

    # Unicidade (ignorando o próprio aluno)
    if _matricula_em_uso(matricula, ignorar_id=id_aluno):
        return (ERRO_ID_REPETIDO, None)
    if _email_em_uso(email, ignorar_id=id_aluno):
        return (ERRO_ID_REPETIDO, None)

    aluno['nome']            = str(nome).strip()
    aluno['data_nascimento'] = str(data_nascimento).strip()
    aluno['matricula']       = matricula
    aluno['curso']           = str(curso).strip()
    aluno['email']           = email
    return (SUCESSO, None)


def remover_aluno(id_aluno):
    """
    Remove um aluno do sistema se não houver empréstimos ativos.
    Retorna (codigo, None).
    Depende do módulo Empréstimo para verificar vínculos.
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, None)

    # Importação local para evitar importação circular
    try:
        import emprestimo
        codigo, existe = emprestimo.existe_emprestimo_ativo_aluno(id_aluno)
        # codigo 0 = existe empréstimo ativo
        if codigo == SUCESSO:
            return (ERRO_OPERACAO_INVALIDA, None)
    except ImportError:
        # Módulo empréstimo ainda não disponível (usado em testes isolados)
        pass

    alunos.remove(aluno)
    return (SUCESSO, None)


def aluno_existe(id_aluno):
    """
    Verifica se um aluno está cadastrado.
    Retorna (codigo, existe:bool).
    """
    if _buscar_aluno(id_aluno) is not None:
        return (SUCESSO, True)
    return (ERRO_ID_INEXISTENTE, False)


def aluno_esta_ativo(id_aluno):
    """
    Verifica se o aluno está ativo para operações de empréstimo.
    Retorna (codigo, ativo:bool).
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, False)
    if aluno['ativo']:
        return (SUCESSO, True)
    return (ERRO_INATIVO, False)


def aluno_pode_pegar_emprestimo(id_aluno):
    """
    Verifica se o aluno pode receber um novo empréstimo:
    deve existir, estar ativo, não ter atingido o limite e
    não ter pendência por atraso.
    Retorna (codigo, pode:bool).
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, False)

    if not aluno['ativo']:
        # Distingue atraso de inatividade genérica via flag auxiliar
        if aluno.get('tem_atraso', False):
            return (ERRO_ATRASO, False)
        return (ERRO_INATIVO, False)

    if aluno['qtd_emprestimos_ativos'] >= aluno['max_emprestimos_ativos']:
        return (ERRO_LIMITE_ATINGIDO, False)

    return (SUCESSO, True)


def incrementar_emprestimos_ativos(id_aluno):
    """
    Incrementa em 1 a quantidade de empréstimos ativos do aluno.
    Retorna (codigo, None).
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, None)

    if aluno['qtd_emprestimos_ativos'] >= aluno['max_emprestimos_ativos']:
        return (ERRO_LIMITE_ATINGIDO, None)

    aluno['qtd_emprestimos_ativos'] += 1
    return (SUCESSO, None)


def decrementar_emprestimos_ativos(id_aluno):
    """
    Decrementa em 1 a quantidade de empréstimos ativos do aluno.
    Retorna (codigo, None).
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, None)

    if aluno['qtd_emprestimos_ativos'] <= 0:
        return (ERRO_OPERACAO_INVALIDA, None)

    aluno['qtd_emprestimos_ativos'] -= 1
    return (SUCESSO, None)


def registrar_atraso_aluno(id_aluno):
    """
    Registra penalidade de atraso: inativa o aluno.
    Retorna (codigo, None).
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, None)

    if not aluno['ativo']:
        return (ERRO_OPERACAO_INVALIDA, None)

    aluno['ativo']     = False
    aluno['tem_atraso'] = True
    return (SUCESSO, None)


def consultar_email_aluno(id_aluno):
    """
    Retorna o e-mail de um aluno cadastrado.
    Retorna (codigo, email) ou (codigo, None).
    """
    aluno = _buscar_aluno(id_aluno)
    if aluno is None:
        return (ERRO_ID_INEXISTENTE, None)
    return (SUCESSO, aluno['email'])


def listar_alunos():
    """
    Lista todos os alunos cadastrados.
    Retorna (codigo, lista_alunos).
    """
    if not alunos:
        return (ERRO_LISTA_VAZIA, [])
    return (SUCESSO, [dict(a) for a in alunos])

