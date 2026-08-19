from rest_framework import serializers

from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    def validate_titulo(self, value):
        titulo = (value or "").strip()
        if not titulo:
            raise serializers.ValidationError("O título é obrigatório.")
        return titulo

    class Meta:
        model = Chamado

        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]

        extra_kwargs = {
            "titulo": {
                "required": True,
                "allow_blank": False,
                "error_messages": {
                    "required": "O título é obrigatório.",
                    "blank": "O título é obrigatório.",
                    "null": "O título é obrigatório.",
                },
            },
        }

        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]
