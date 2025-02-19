from django.contrib import admin
from .models import Paciente, Consulta, Tarefa


admin.site.register(Paciente)
admin.site.register(Consulta)
admin.site.register(Tarefa)
