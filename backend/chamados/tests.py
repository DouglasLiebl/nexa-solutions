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

