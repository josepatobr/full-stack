# Generated by Django 5.1.6 on 2025-02-17 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_tarefas_consultas_visualizacoes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Consultas',
            new_name='Consulta',
        ),
        migrations.RenameModel(
            old_name='Pacientes',
            new_name='Paciente',
        ),
        migrations.RenameModel(
            old_name='Tarefas',
            new_name='Tarefa',
        ),
        migrations.RenameModel(
            old_name='Visualizacoes',
            new_name='Visualizacao',
        ),
    ]
