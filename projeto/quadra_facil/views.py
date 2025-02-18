from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Quadra, Horario, Reserva
from .serializers import QuadraSerializer, ReservaSerializer, HorarioSerializer

class QuadraView(APIView):
    def get(self, request, format=None):
        quadras = Quadra.objects.all()
        serializer = QuadraSerializer(quadras, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuadraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HorarioView(APIView):

    def get(self, request, quadra_id, format=None):
        try:
            # Verifica se a quadra existe
            quadra = Quadra.objects.get(id=quadra_id)
        except Quadra.DoesNotExist:
            return Response({'error': 'Quadra não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        # Obtém todos os horários disponíveis dessa quadra
        horarios = Horario.objects.filter(quadra=quadra, status='disponivel')
        serializer = HorarioSerializer(horarios, many=True)
        return Response(serializer.data)

    def post(self, request, quadra_id, format=None):
        try:
            # Verifica se a quadra existe
            quadra = Quadra.objects.get(id=quadra_id)
        except Quadra.DoesNotExist:
            return Response({'error': 'Quadra não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        # Adiciona o ID da quadra nos dados da requisição para criar o horário
        data = request.data
        data['quadra'] = quadra.id

        # Cria o horário com os dados recebidos
        serializer = HorarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReservaView(APIView):
    def get(self, request, format=None):
        # Se passar o ID do horário, retorna as reservas daquele horário
        horario_id = request.query_params.get('horario_id', None)
        if horario_id:
            try:
                horario = Horario.objects.get(id=horario_id)
                reservas = Reserva.objects.filter(horario=horario)
            except Horario.DoesNotExist:
                return Response({'error': 'Horário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Caso contrário, retorna todas as reservas
            reservas = Reserva.objects.all()

        # Serializa as reservas e retorna a resposta
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        # Coleta dados da reserva
        horario_id = request.data.get('horario')
        nome_reservante = request.data.get('nome_reservante')
        telefone_reservante = request.data.get('telefone_reservante')

        # Verifica se o horário existe
        try:
            horario = Horario.objects.get(id=horario_id)
        except Horario.DoesNotExist:
            return Response({'error': 'Horário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se o horário está disponível
        if horario.status == 'reservado':
            return Response({'error': 'Horário já reservado'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Cria a reserva
        reserva = Reserva.objects.create(
            horario=horario,
            nome_reservante=nome_reservante,
            telefone_reservante=telefone_reservante
        )
        
        # Atualiza o status do horário para reservado
        horario.status = 'reservado'
        horario.save()

        # Envia a mensagem de WhatsApp
        #self.enviar_whatsapp(nome_reservante, telefone_reservante, horario)

        # Retorna os dados da reserva criada
        serializer = ReservaSerializer(reserva)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
