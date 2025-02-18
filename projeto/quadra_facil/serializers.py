from rest_framework import serializers
from .models import Quadra, Horario, Reserva

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ['id', 'horario_inicio', 'horario_fim', 'status']

class QuadraSerializer(serializers.ModelSerializer):
    horarios_disponiveis = HorarioSerializer(many=True, read_only=True)

    class Meta:
        model = Quadra
        fields = ['id', 'nome', 'descricao', 'endereco', 'horarios_disponiveis']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'horario', 'nome_reservante', 'telefone_reservante', 'data_reserva']