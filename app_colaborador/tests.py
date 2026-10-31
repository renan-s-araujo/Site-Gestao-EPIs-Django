from django.test import TestCase
from django.urls import reverse

from .models import Colaborador, Equipamento, Emprestimo


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
