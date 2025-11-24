from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Tarea
from .forms import TareaForm, RegisterForm


# ---------------------------
# REGISTRO DE USUARIO
# ---------------------------

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tareas:task_list')
    else:
        form = RegisterForm()

    return render(request, 'tareas/register.html', {'form': form})


# ---------------------------
# LISTAR TAREAS
# ---------------------------

@login_required
def task_list(request):
    tareas = Tarea.objects.filter(user=request.user)
    return render(request, 'tareas/task_list.html', {'tasks': tareas})


# ---------------------------
# CREAR TAREA
# ---------------------------

@login_required
def task_add(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.user = request.user   # asignar usuario dueño de la tarea
            tarea.save()
            return redirect('tareas:task_list')
    else:
        form = TareaForm()

    return render(request, 'tareas/task_form.html', {
        'form': form,
        'edit_mode': False
    })


# ---------------------------
# EDITAR TAREA
# ---------------------------

@login_required
def task_edit(request, task_id):
    tarea = get_object_or_404(Tarea, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('tareas:task_list')
    else:
        form = TareaForm(instance=tarea)

    return render(request, 'tareas/task_form.html', {
        'form': form,
        'edit_mode': True,
        'task': tarea
    })


# ---------------------------
# VER DETALLE DE UNA TAREA
# ---------------------------

@login_required
def task_detail(request, task_id):
    tarea = get_object_or_404(Tarea, id=task_id, user=request.user)
    return render(request, 'tareas/task_detail.html', {'task': tarea})


# ---------------------------
# ELIMINAR TAREA
# ---------------------------

@login_required
def task_delete(request, task_id):
    tarea = get_object_or_404(Tarea, id=task_id, user=request.user)

    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas:task_list')

    return render(request, 'tareas/task_delete.html', {'task': tarea})
