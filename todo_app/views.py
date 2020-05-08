from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todos


def home(request):
    return render(request, 'todo/home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error':'User ID has been already taken..'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error':'Password didnt match..'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and password didnt match.. '})
        else:
            login(request, user)
            return redirect('currenttodos')


def createtodo(request):
    if request.method=='GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad Data.. Try again..'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')



def currenttodos(request):
    todos = Todos.objects.filter(user=request.user, datecompleted__isnull = True)
    return render(request, 'todo/currenttodos.html', {'todos':todos} )


def viewtodo(request, todo_pk):
    todo  = get_object_or_404(Todos, pk=todo_pk)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/current.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/current.html', {'todo':todo, 'form':form, 'error':'Bad Data.. Try again..'})
