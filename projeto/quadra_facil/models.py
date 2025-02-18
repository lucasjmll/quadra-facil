from django.db import models

class Quadra(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    endereco = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'quadra'

    def __str__(self):
        return self.nome

class Horario(models.Model):
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, related_name='horarios_disponiveis')
    horario_inicio = models.DateTimeField()  
    horario_fim = models.DateTimeField()    
    status = models.CharField(max_length=20, choices=[('disponivel', 'Disponível'), ('reservado', 'Reservado')], default='disponivel')

    class Meta:
        db_table = 'horario'

    def __str__(self):
        return f"Disponibilidade de {self.quadra.nome} de {self.horario_inicio} até {self.horario_fim}"
    
class Reserva(models.Model):
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='reservas')
    nome_reservante = models.CharField(max_length=255)
    telefone_reservante = models.CharField(max_length=15)
    data_reserva = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reserva'

    def __str__(self):
        quadra_nome = self.horario.quadra.nome
        return f"Reserva de {self.nome_reservante} para {quadra_nome} em {self.data_reserva}"
