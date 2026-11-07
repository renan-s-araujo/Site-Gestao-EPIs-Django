from django.test import TestCase
from django.urls import reverse

from .models import Colaborador, Equipamento, Emprestimo
from django.contrib.auth import get_user_model


class CadastroUsuarioTests(TestCase):
    def dados(self, **alteracoes):
        dados = {'username': 'ana.teste', 'email': 'ana@example.com',
                 'password1': 'Segura!4729az', 'password2': 'Segura!4729az'}
        dados.update(alteracoes)
        return dados

    def test_tela_e_link_do_login(self):
        self.assertContains(self.client.get(reverse('cadastro_usuario')), 'Crie sua conta')
        self.assertContains(self.client.get(reverse('login')), 'href="/cadastro/"')

    def test_cadastro_salva_email_e_senha_e_permite_login(self):
        resposta = self.client.post(reverse('cadastro_usuario'), self.dados(), follow=True)
        self.assertRedirects(resposta, reverse('login'))
        self.assertContains(resposta, 'Conta criada com sucesso!')
        usuario = get_user_model().objects.get(username='ana.teste')
        self.assertEqual(usuario.email, 'ana@example.com')
        self.assertTrue(usuario.check_password('Segura!4729az'))
        self.assertFalse(usuario.is_staff)
        self.assertTrue(self.client.login(username='ana.teste', password='Segura!4729az'))
        self.assertEqual(self.client.get(reverse('lista_colaboradores')).status_code, 200)

    def test_dados_invalidos_nao_criam_usuario(self):
        for alteracoes in [{'email': 'invalido'}, {'email': ''},
                           {'password2': 'Outra!4729az'},
                           {'password1': '123', 'password2': '123'}]:
            with self.subTest(alteracoes=alteracoes):
                resposta = self.client.post(reverse('cadastro_usuario'), self.dados(**alteracoes))
                self.assertEqual(resposta.status_code, 200)
                self.assertTrue(resposta.context['formulario'].errors)
                self.assertFalse(get_user_model().objects.exists())

    def test_usuario_duplicado_e_rejeitado(self):
        get_user_model().objects.create_user(username='ana.teste', password='Segura!4729az')
        resposta = self.client.post(reverse('cadastro_usuario'), self.dados())
        self.assertIn('username', resposta.context['formulario'].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_anonimo_nao_acessa_sistema(self):
        for nome in ['index', 'lista_colaboradores', 'lista_equipamentos', 'lista_emprestimos']:
            resposta = self.client.get(reverse(nome))
            self.assertEqual(resposta.status_code, 302)
            self.assertTrue(resposta.url.startswith(reverse('login')))

    def test_autenticado_nao_cadastra_nova_conta(self):
        usuario = get_user_model().objects.create_user(username='existente')
        self.client.force_login(usuario)
        resposta = self.client.post(reverse('cadastro_usuario'), self.dados())
        self.assertRedirects(resposta, reverse('lista_colaboradores'))
        self.assertEqual(get_user_model().objects.count(), 1)


class RelatorioEmprestimosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ana = Colaborador.objects.create(nome='Ana Silva', cargo='Técnica', setor='Produção')
        bruno = Colaborador.objects.create(nome='Bruno Souza', cargo='Técnico', setor='Produção')
        capacete = Equipamento.objects.create(ca='123', nome='Capacete azul', tipo='Capacete')
        oculos = Equipamento.objects.create(ca='456', nome='Óculos de proteção', tipo='Óculos')
        cls.alvo = Emprestimo.objects.create(colaborador=ana, equipamento=capacete, status='Emprestado')
        Emprestimo.objects.create(colaborador=ana, equipamento=capacete, status='Devolvido')
        Emprestimo.objects.create(colaborador=ana, equipamento=oculos, status='Emprestado')
        Emprestimo.objects.create(colaborador=bruno, equipamento=capacete, status='Emprestado')

    def test_sem_filtros_exibe_historico_completo(self):
        resposta = self.client.get(reverse('lista_emprestimos'))
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['emprestimos'].count(), 4)

    def test_filtros_individuais(self):
        for filtros, quantidade in [
            ({'colaborador': ' ANA '}, 3),
            ({'equipamento': 'capacete'}, 3),
            ({'status': 'Devolvido'}, 1),
        ]:
            with self.subTest(filtros=filtros):
                resposta = self.client.get(reverse('lista_emprestimos'), filtros)
                self.assertEqual(resposta.context['emprestimos'].count(), quantidade)

    def test_filtros_combinados_usam_and_e_preservam_selecao(self):
        resposta = self.client.get(reverse('lista_emprestimos'), {
            'colaborador': 'Ana', 'equipamento': 'capacete', 'status': 'Emprestado',
        })
        self.assertEqual(list(resposta.context['emprestimos']), [self.alvo])
        self.assertEqual(resposta.context['total_emprestimos'], 4)
        self.assertContains(resposta, 'value="Ana"')
        self.assertContains(resposta, 'value="capacete"')
        self.assertContains(resposta, 'value="Emprestado" selected')

    def test_sem_resultados(self):
        resposta = self.client.get(reverse('lista_emprestimos'), {
            'colaborador': 'Bruno', 'status': 'Devolvido',
        })
        self.assertContains(resposta, 'Nenhum empréstimo encontrado.')

    def test_status_invalido_e_ignorado(self):
        resposta = self.client.get(reverse('lista_emprestimos'), {'status': 'inexistente'})
        self.assertEqual(resposta.context['emprestimos'].count(), 4)
        self.assertEqual(resposta.context['status_filtro'], '')
