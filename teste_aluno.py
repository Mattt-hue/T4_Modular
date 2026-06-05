import unittest
import sys
import os

# Garante que o módulo aluno.py seja encontrado
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import aluno
from aluno import *

# ---------------------------------------------------------------------------
# Códigos de retorno (espelhando o módulo)
# ---------------------------------------------------------------------------
SUCESSO                = 0
ERRO_ID_INEXISTENTE    = 1
ERRO_ID_REPETIDO       = 2
ERRO_DADOS_INVALIDOS   = 3
ERRO_OPERACAO_INVALIDA = 4
ERRO_LIMITE_ATINGIDO   = 5
ERRO_INATIVO           = 7
ERRO_ATRASO            = 8
ERRO_LISTA_VAZIA       = 9


class TestModuloAluno(unittest.TestCase):

    def setUp(self):
        """Limpa a lista de alunos antes de cada teste."""
        aluno.alunos.clear()

    # -----------------------------------------------------------------------
    # cadastrar_aluno — A01, A02, A03, A04
    # -----------------------------------------------------------------------

    def test_A01_cadastrar_aluno_sucesso(self):
        print("Caso de Teste A01 - Cadastrar aluno com sucesso")
        codigo, _ = cadastrar_aluno(
            'A1', 'Matheus', '2000-01-01', '2410520',
            'Engenharia', 'matheus@puc.br', 'senha123'
        )
        self.assertEqual(codigo, SUCESSO)

    def test_A02_cadastrar_aluno_id_repetido(self):
        print("Caso de Teste A02 - Cadastrar com id_aluno já existente")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, _ = cadastrar_aluno(
            'A1', 'Outro', '1999-05-10', '9999999',
            'Direito', 'outro@puc.br', 'outra123'
        )
        self.assertEqual(codigo, ERRO_ID_REPETIDO)

    def test_A03_cadastrar_aluno_matricula_ou_email_repetido(self):
        print("Caso de Teste A03 - Cadastrar com matrícula ou e-mail já existente")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        # Mesma matrícula
        codigo, _ = cadastrar_aluno(
            'A2', 'Outro', '1999-05-10', '2410520',
            'Direito', 'outro@puc.br', 'outra123'
        )
        self.assertEqual(codigo, ERRO_ID_REPETIDO)
        # Mesmo e-mail
        codigo2, _ = cadastrar_aluno(
            'A3', 'Terceiro', '1998-03-20', '1111111',
            'Medicina', 'matheus@puc.br', 'senha456'
        )
        self.assertEqual(codigo2, ERRO_ID_REPETIDO)

    def test_A04_cadastrar_aluno_dados_invalidos(self):
        print("Caso de Teste A04 - Cadastrar com dados inválidos ou vazios")
        # Nome vazio
        codigo, _ = cadastrar_aluno('A1', '', '2000-01-01', '2410520',
                                    'Engenharia', 'mat@puc.br', 'senha123')
        self.assertEqual(codigo, ERRO_DADOS_INVALIDOS)
        # Senha vazia
        codigo2, _ = cadastrar_aluno('A2', 'Matheus', '2000-01-01', '2410521',
                                     'Engenharia', 'mat2@puc.br', '')
        self.assertEqual(codigo2, ERRO_DADOS_INVALIDOS)
        # E-mail inválido
        codigo3, _ = cadastrar_aluno('A3', 'Matheus', '2000-01-01', '2410522',
                                     'Engenharia', 'emailinvalido', 'senha123')
        self.assertEqual(codigo3, ERRO_DADOS_INVALIDOS)

    # -----------------------------------------------------------------------
    # validar_login — A05, A06, A07, A08
    # -----------------------------------------------------------------------

    def test_A05_validar_login_sucesso(self):
        print("Caso de Teste A05 - Login com sucesso")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, id_retornado = validar_login('2410520', 'senha123')
        self.assertEqual(codigo, SUCESSO)
        self.assertEqual(id_retornado, 'A1')

    def test_A06_validar_login_matricula_inexistente(self):
        print("Caso de Teste A06 - Login com matrícula inexistente")
        codigo, _ = validar_login('9999999', 'senha123')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)

    def test_A07_validar_login_dados_invalidos(self):
        print("Caso de Teste A07 - Login com matrícula ou senha vazia")
        codigo, _ = validar_login('', 'senha123')
        self.assertEqual(codigo, ERRO_DADOS_INVALIDOS)
        codigo2, _ = validar_login('2410520', '')
        self.assertEqual(codigo2, ERRO_DADOS_INVALIDOS)

    def test_A08_validar_login_senha_incorreta(self):
        print("Caso de Teste A08 - Login com senha incorreta")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, _ = validar_login('2410520', 'senhaErrada')
        self.assertEqual(codigo, ERRO_OPERACAO_INVALIDA)

    # -----------------------------------------------------------------------
    # consultar_aluno — A09, A10
    # -----------------------------------------------------------------------

    def test_A09_consultar_aluno_sucesso(self):
        print("Caso de Teste A09 - Consultar aluno existente")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, dados = consultar_aluno('A1')
        self.assertEqual(codigo, SUCESSO)
        self.assertEqual(dados['id_aluno'], 'A1')
        self.assertEqual(dados['nome'], 'Matheus')

    def test_A10_consultar_aluno_inexistente(self):
        print("Caso de Teste A10 - Consultar aluno inexistente")
        codigo, dados = consultar_aluno('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)
        self.assertIsNone(dados)

    # -----------------------------------------------------------------------
    # atualizar_aluno — A11, A12, A13, A14
    # -----------------------------------------------------------------------

    def test_A11_atualizar_aluno_sucesso(self):
        print("Caso de Teste A11 - Atualizar aluno com sucesso")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, _ = atualizar_aluno('A1', 'Matheus Novo', '2000-02-02',
                                    '2410520', 'Ciência da Computação',
                                    'novo@puc.br')
        self.assertEqual(codigo, SUCESSO)
        _, dados = consultar_aluno('A1')
        self.assertEqual(dados['nome'], 'Matheus Novo')

    def test_A12_atualizar_aluno_inexistente(self):
        print("Caso de Teste A12 - Atualizar aluno inexistente")
        codigo, _ = atualizar_aluno('INEXISTENTE', 'Nome', '2000-01-01',
                                    '9999999', 'Curso', 'x@x.com')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)

    def test_A13_atualizar_aluno_matricula_email_repetido(self):
        print("Caso de Teste A13 - Atualizar com matrícula/e-mail já de outro aluno")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        cadastrar_aluno('A2', 'Arthur', '2001-06-15', '2510339',
                        'Computação', 'arthur@puc.br', 'senha456')
        # Tenta usar matrícula do A2
        codigo, _ = atualizar_aluno('A1', 'Matheus', '2000-01-01',
                                    '2510339', 'Engenharia', 'novo@puc.br')
        self.assertEqual(codigo, ERRO_ID_REPETIDO)
        # Tenta usar e-mail do A2
        codigo2, _ = atualizar_aluno('A1', 'Matheus', '2000-01-01',
                                     '2410520', 'Engenharia', 'arthur@puc.br')
        self.assertEqual(codigo2, ERRO_ID_REPETIDO)

    def test_A14_atualizar_aluno_dados_invalidos(self):
        print("Caso de Teste A14 - Atualizar aluno com dados inválidos")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, _ = atualizar_aluno('A1', '', '2000-01-01',
                                    '2410520', 'Engenharia', 'matheus@puc.br')
        self.assertEqual(codigo, ERRO_DADOS_INVALIDOS)
        codigo2, _ = atualizar_aluno('A1', 'Matheus', '2000-01-01',
                                     '2410520', 'Engenharia', 'emailinvalido')
        self.assertEqual(codigo2, ERRO_DADOS_INVALIDOS)

    # -----------------------------------------------------------------------
    # remover_aluno — A15, A16, A17
    # -----------------------------------------------------------------------

    def test_A15_remover_aluno_sucesso(self):
        print("Caso de Teste A15 - Remover aluno sem empréstimos ativos")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, _ = remover_aluno('A1')
        self.assertEqual(codigo, SUCESSO)
        self.assertEqual(len(aluno.alunos), 0)

    def test_A16_remover_aluno_inexistente(self):
        print("Caso de Teste A16 - Remover aluno inexistente")
        codigo, _ = remover_aluno('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)

    def test_A17_remover_aluno_com_emprestimo_ativo(self):
        print("Caso de Teste A17 - Remover aluno com empréstimo ativo (simulado)")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        # Simula empréstimo ativo incrementando o contador
        incrementar_emprestimos_ativos('A1')
        # Injeta stub no módulo emprestimo para simular existência de empréstimo ativo
        import types
        modulo_stub = types.ModuleType('emprestimo')
        modulo_stub.existe_emprestimo_ativo_aluno = lambda id_a: (SUCESSO, True)
        sys.modules['emprestimo'] = modulo_stub
        codigo, _ = remover_aluno('A1')
        self.assertEqual(codigo, ERRO_OPERACAO_INVALIDA)
        # Remove stub após o teste
        del sys.modules['emprestimo']

    # -----------------------------------------------------------------------
    # aluno_existe — A18, A19
    # -----------------------------------------------------------------------

    def test_A18_aluno_existe_sucesso(self):
        print("Caso de Teste A18 - Verificar existência de aluno existente")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, existe = aluno_existe('A1')
        self.assertEqual(codigo, SUCESSO)
        self.assertTrue(existe)

    def test_A19_aluno_existe_inexistente(self):
        print("Caso de Teste A19 - Verificar existência de aluno inexistente")
        codigo, existe = aluno_existe('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)
        self.assertFalse(existe)

    # -----------------------------------------------------------------------
    # aluno_esta_ativo — A20, A21, A22
    # -----------------------------------------------------------------------

    def test_A20_aluno_esta_ativo_ativo(self):
        print("Caso de Teste A20 - Aluno existente e ativo")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, ativo = aluno_esta_ativo('A1')
        self.assertEqual(codigo, SUCESSO)
        self.assertTrue(ativo)

    def test_A21_aluno_esta_ativo_inexistente(self):
        print("Caso de Teste A21 - Verificar atividade de aluno inexistente")
        codigo, ativo = aluno_esta_ativo('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)
        self.assertFalse(ativo)

    def test_A22_aluno_esta_ativo_inativo(self):
        print("Caso de Teste A22 - Aluno existente e inativo")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        registrar_atraso_aluno('A1')  # inativa o aluno
        codigo, ativo = aluno_esta_ativo('A1')
        self.assertEqual(codigo, ERRO_INATIVO)
        self.assertFalse(ativo)

    # -----------------------------------------------------------------------
    # aluno_pode_pegar_emprestimo — A23, A24, A25, A26, A27
    # -----------------------------------------------------------------------

    def test_A23_aluno_pode_pegar_emprestimo_sucesso(self):
        print("Caso de Teste A23 - Aluno apto a pegar empréstimo")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, pode = aluno_pode_pegar_emprestimo('A1')
        self.assertEqual(codigo, SUCESSO)
        self.assertTrue(pode)

    def test_A24_aluno_pode_pegar_emprestimo_inexistente(self):
        print("Caso de Teste A24 - Aluno inexistente não pode pegar empréstimo")
        codigo, pode = aluno_pode_pegar_emprestimo('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)
        self.assertFalse(pode)

    def test_A25_aluno_pode_pegar_emprestimo_limite_atingido(self):
        print("Caso de Teste A25 - Aluno com limite máximo de empréstimos atingido")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        # Forçar 3 empréstimos ativos
        aluno._buscar_aluno('A1')['qtd_emprestimos_ativos'] = 3
        codigo, pode = aluno_pode_pegar_emprestimo('A1')
        self.assertEqual(codigo, ERRO_LIMITE_ATINGIDO)
        self.assertFalse(pode)

    def test_A26_aluno_pode_pegar_emprestimo_inativo(self):
        print("Caso de Teste A26 - Aluno inativo não pode pegar empréstimo")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        # Inativar sem atraso (forçar diretamente)
        aluno._buscar_aluno('A1')['ativo'] = False
        aluno._buscar_aluno('A1')['tem_atraso'] = False
        codigo, pode = aluno_pode_pegar_emprestimo('A1')
        self.assertEqual(codigo, ERRO_INATIVO)
        self.assertFalse(pode)

    def test_A27_aluno_pode_pegar_emprestimo_atraso(self):
        print("Caso de Teste A27 - Aluno com pendência de atraso")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        registrar_atraso_aluno('A1')
        codigo, pode = aluno_pode_pegar_emprestimo('A1')
        self.assertEqual(codigo, ERRO_ATRASO)
        self.assertFalse(pode)

    # -----------------------------------------------------------------------
    # incrementar_emprestimos_ativos — A28, A29, A30
    # -----------------------------------------------------------------------

    def test_A28_incrementar_emprestimos_ativos_sucesso(self):
        print("Caso de Teste A28 - Incrementar empréstimos ativos com sucesso")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, _ = incrementar_emprestimos_ativos('A1')
        self.assertEqual(codigo, SUCESSO)
        _, dados = consultar_aluno('A1')
        self.assertEqual(dados['qtd_emprestimos_ativos'], 1)

    def test_A29_incrementar_emprestimos_ativos_inexistente(self):
        print("Caso de Teste A29 - Incrementar empréstimos de aluno inexistente")
        codigo, _ = incrementar_emprestimos_ativos('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)

    def test_A30_incrementar_emprestimos_ativos_limite(self):
        print("Caso de Teste A30 - Incrementar além do limite máximo")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        aluno._buscar_aluno('A1')['qtd_emprestimos_ativos'] = 3
        codigo, _ = incrementar_emprestimos_ativos('A1')
        self.assertEqual(codigo, ERRO_LIMITE_ATINGIDO)

    # -----------------------------------------------------------------------
    # decrementar_emprestimos_ativos — A31, A32, A33
    # -----------------------------------------------------------------------

    def test_A31_decrementar_emprestimos_ativos_sucesso(self):
        print("Caso de Teste A31 - Decrementar empréstimos ativos com sucesso")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        incrementar_emprestimos_ativos('A1')
        codigo, _ = decrementar_emprestimos_ativos('A1')
        self.assertEqual(codigo, SUCESSO)
        _, dados = consultar_aluno('A1')
        self.assertEqual(dados['qtd_emprestimos_ativos'], 0)

    def test_A32_decrementar_emprestimos_ativos_inexistente(self):
        print("Caso de Teste A32 - Decrementar empréstimos de aluno inexistente")
        codigo, _ = decrementar_emprestimos_ativos('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)

    def test_A33_decrementar_emprestimos_ativos_zero(self):
        print("Caso de Teste A33 - Decrementar com 0 empréstimos ativos")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, _ = decrementar_emprestimos_ativos('A1')
        self.assertEqual(codigo, ERRO_OPERACAO_INVALIDA)

    # -----------------------------------------------------------------------
    # registrar_atraso_aluno — A34, A35, A36
    # -----------------------------------------------------------------------

    def test_A34_registrar_atraso_aluno_sucesso(self):
        print("Caso de Teste A34 - Registrar atraso de aluno ativo")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, _ = registrar_atraso_aluno('A1')
        self.assertEqual(codigo, SUCESSO)
        _, dados = consultar_aluno('A1')
        self.assertFalse(dados['ativo'])
        self.assertTrue(dados['tem_atraso'])

    def test_A35_registrar_atraso_aluno_inexistente(self):
        print("Caso de Teste A35 - Registrar atraso de aluno inexistente")
        codigo, _ = registrar_atraso_aluno('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)

    def test_A36_registrar_atraso_aluno_ja_inativo(self):
        print("Caso de Teste A36 - Registrar atraso de aluno já inativo")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        registrar_atraso_aluno('A1')  # primeira inativação
        codigo, _ = registrar_atraso_aluno('A1')  # segunda tentativa
        self.assertEqual(codigo, ERRO_OPERACAO_INVALIDA)

    # -----------------------------------------------------------------------
    # consultar_email_aluno — A37, A38
    # -----------------------------------------------------------------------

    def test_A37_consultar_email_aluno_sucesso(self):
        print("Caso de Teste A37 - Consultar e-mail de aluno existente")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        codigo, email = consultar_email_aluno('A1')
        self.assertEqual(codigo, SUCESSO)
        self.assertEqual(email, 'matheus@puc.br')

    def test_A38_consultar_email_aluno_inexistente(self):
        print("Caso de Teste A38 - Consultar e-mail de aluno inexistente")
        codigo, email = consultar_email_aluno('INEXISTENTE')
        self.assertEqual(codigo, ERRO_ID_INEXISTENTE)
        self.assertIsNone(email)

    # -----------------------------------------------------------------------
    # listar_alunos — A39, A40
    # -----------------------------------------------------------------------

    def test_A39_listar_alunos_sucesso(self):
        print("Caso de Teste A39 - Listar alunos com registros cadastrados")
        cadastrar_aluno('A1', 'Matheus', '2000-01-01', '2410520',
                        'Engenharia', 'matheus@puc.br', 'senha123')
        cadastrar_aluno('A2', 'Arthur', '2001-06-15', '2510339',
                        'Computação', 'arthur@puc.br', 'senha456')
        codigo, lista = listar_alunos()
        self.assertEqual(codigo, SUCESSO)
        self.assertEqual(len(lista), 2)
        ids = [a['id_aluno'] for a in lista]
        self.assertIn('A1', ids)
        self.assertIn('A2', ids)

    def test_A40_listar_alunos_lista_vazia(self):
        print("Caso de Teste A40 - Listar alunos sem nenhum cadastrado")
        codigo, lista = listar_alunos()
        self.assertEqual(codigo, ERRO_LISTA_VAZIA)
        self.assertEqual(lista, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)

