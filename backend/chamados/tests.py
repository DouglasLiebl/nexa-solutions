from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chamados.models import Chamado


class CadastroChamadoSemTituloTests(APITestCase):
    def setUp(self):
        self.url = reverse("chamado-list-create")

    def test_nao_cria_chamado_sem_campo_titulo(self):
        resposta = self.client.post(
            self.url,
            {"descricao": "Chamado sem título"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(resposta.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("titulo", resposta.json())
        self.assertIn("obrigatório", str(resposta.json()["titulo"]).lower())
        self.assertEqual(Chamado.objects.count(), 0)

    def test_nao_cria_chamado_com_titulo_vazio(self):
        resposta = self.client.post(
            self.url,
            {"titulo": "", "descricao": "Chamado sem título"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(resposta.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("titulo", resposta.json())
        self.assertIn("obrigatório", str(resposta.json()["titulo"]).lower())
        self.assertEqual(Chamado.objects.count(), 0)

    def test_nao_cria_chamado_com_titulo_apenas_espacos(self):
        resposta = self.client.post(
            self.url,
            {"titulo": "   ", "descricao": "Chamado sem título"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", resposta.json())
        self.assertEqual(Chamado.objects.count(), 0)


class FiltroChamadoPorStatusTests(APITestCase):
    def setUp(self):
        self.url = reverse("chamado-list-create")
        Chamado.objects.create(
            titulo="Impressora com defeito",
            status=Chamado.Status.ABERTO,
        )
        Chamado.objects.create(titulo="Acesso à VPN", status=Chamado.Status.ABERTO)
        Chamado.objects.create(
            titulo="Troca de notebook",
            status=Chamado.Status.EM_ANDAMENTO,
        )
        Chamado.objects.create(
            titulo="Instalação de software",
            status=Chamado.Status.CONCLUIDO,
        )

    def test_filtra_somente_chamados_abertos(self):
        resposta = self.client.get(self.url, {"status": "ABERTO"})

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        chamados = resposta.json()
        self.assertEqual(len(chamados), 2)
        self.assertTrue(all(chamado["status"] == "ABERTO" for chamado in chamados))
        self.assertEqual(
            {chamado["titulo"] for chamado in chamados},
            {"Impressora com defeito", "Acesso à VPN"},
        )

    def test_filtra_chamados_em_andamento(self):
        resposta = self.client.get(self.url, {"status": "EM_ANDAMENTO"})

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        chamados = resposta.json()
        self.assertEqual(len(chamados), 1)
        self.assertEqual(chamados[0]["status"], "EM_ANDAMENTO")

    def test_sem_filtro_retorna_todos_os_chamados(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.json()), 4)

    def test_status_invalido_retorna_400(self):
        resposta = self.client.get(self.url, {"status": "INVALIDO"})

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(resposta.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("status", resposta.json())
        self.assertEqual(Chamado.objects.count(), 4)

