from django.shortcuts import render, redirect
from .models import Paciente, Consulta, Tarefa
from django.contrib import messages
from django.http import HttpRequest, Http404


def pacientes(request: HttpRequest):
    if request.method == "GET":
        pacientes_list = Paciente.objects.all()
        return render(
                request,
                "pacientes.html",
                {"queixas": Paciente.queixa_choices, "pacientes": pacientes_list},
                    )
    
    nome = request.POST.get("nome")
    email = request.POST.get("email")
    telefone = request.POST.get("telefone")
    queixa = request.POST.get("queixa")
    foto = request.FILES.get("foto")

    if len(nome.strip()) == 0 or not foto:
        messages.error(request, "O campo nome e foto são obrigatórios")

        return redirect("pacientes")

    paciente = Paciente.objects.create(
        nome=nome, email=email, telefone=telefone, queixa=queixa, foto=foto)
    paciente.save()

    messages.success(request, "Paciente adicionado com sucesso")
    return redirect("pacientes")


def paciente_view(request: HttpRequest, id):
    paciente = Paciente.objects.get(id=id)
    if request.method == "GET":
        tarefas = Tarefa.objects.all()
        consultas = Consulta.objects.filter(paciente=paciente)
        tuple_grafico = (
            [str(i.data) for i in consultas],
            [str(i.humor) for i in consultas])

        return render(request, "paciente.html",
            {
                "tarefas": tarefas,
                "paciente": paciente,
                "consultas": consultas,
                "tuple_grafico": tuple_grafico
            },
        )
    humor = request.POST.get("humor")
    registro_geral = request.POST.get("registro_geral")
    video = request.FILES.get("video")
    tarefas = request.POST.getlist("tarefas")

    consultas = Consulta(
        humor=int(humor),
        registro_geral=registro_geral,
        video=video,
        paciente=paciente)
    consultas.save()

    for i in tarefas:
        tarefa = Tarefa.objects.get(id=i)
        consultas.tarefas.add(tarefa)

        consultas.save()

        messages.success(request, "Registro de consulta adicionado com sucesso.")
        return redirect(f"/pacientes/{id}")


def atualizar_paciente(request: HttpRequest, id):
    paciente = Paciente.objects.get(id=id)
    pagamento_em_dia = request.POST.get("pagamento_em_dia")
    status = True if pagamento_em_dia == "ativo" else False
    
    paciente.pagamento_em_dia = status
    paciente.save()
    return redirect(f"/pacientes/{id}")


def excluir_consulta(request: HttpRequest, id:int):
    consulta = Consulta.objects.get(id=id)
    consulta.delete()
    return redirect("paciente_view", id=consulta.paciente.id)


def consulta_publica(request, id):
    consulta = Consulta.objects.get(id=id)
    if not consulta.paciente.pagamento_em_dia:
        raise Http404()

    return render(request, "consulta_publica.html", {"consulta": consulta})
