from django.db import models
from datetime import *
from django.urls import reverse
from urllib.parse import urljoin
from django.conf import settings

BASE_URL = getattr(settings, "BASE_URL", None)


class Paciente(models.Model):
    queixa_choices = (
        ('TDAH', 'TDAH'),
        ('DPS', 'Depressão'),
        ('ASD', 'Ansiedade'),
        ('TAG', 'Transtorno de ansiedade generalizada')
    )

    nome = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=255, null=True, blank=True)
    queixa = models.CharField(max_length=4, choices=queixa_choices, default='TDAH')
    foto = models.ImageField(upload_to='fotos')
    pagamento_em_dia = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class meta:
    verbose_name = "Paciente"
    verbose_name_plural = "Pacientes"


class Tarefa(models.Model):
    frequencia_choices = (
        ('D', 'Diário'),
        ('1S', '1 vez por semana'),
        ('2S', '2 vezes por semana'),
        ('3S', '3 vezes por semana'),
        ('N', 'Ao necessitar')
    )
    tarefa = models.CharField(max_length=255)
    instrucoes = models.TextField()
    frequencia = models.CharField(max_length=2, choices=frequencia_choices, default='D')

    def __str__(self):
        return self.tarefa

class meta:
    verbose_name ="Tarefa"
    verbose_name_plural = "Tarefas"

class Consulta(models.Model):
    humor = models.PositiveIntegerField()
    registro_geral = models.TextField()
    video = models.FileField(upload_to="video")
    tarefas = models.ManyToManyField(Tarefa)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.paciente.nome

    @property
    def link_publico(self):
        return f"http://127.0.0.1:8000{reverse('consulta_publica', kwargs={'id': self.id})}"

class Meta:
    verbose_name = "Consulta"
    verbose_name_plural = "Consultas"
    

class Visualizacao(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()


class Meta:
    verbose_name = "Visualização"
    verbose_name_plural = "Visualizações"


