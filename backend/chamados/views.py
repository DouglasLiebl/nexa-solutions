from rest_framework import generics
from rest_framework.exceptions import ValidationError

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

        status_filtro = status_filtro.strip()
        status_validos = list(Chamado.Status.values)

        if status_filtro not in status_validos:
            raise ValidationError(
                {
                    "status": (
                        "Status inválido. Valores aceitos: "
                        f"{', '.join(status_validos)}."
                    )
                }
            )

        return queryset.filter(status=status_filtro)


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer