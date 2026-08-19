from rest_framework import generics

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoListCreateView(generics.ListCreateAPIView):
    """Lista e cria chamados, com filtro opcional por status."""

    serializer_class = ChamadoSerializer

    def get_queryset(self):
        queryset = Chamado.objects.all().order_by("-criado_em")
        status_filtro = self.request.query_params.get("status")

        if not status_filtro:
            return queryset

        return queryset.filter(status=status_filtro.strip())


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer