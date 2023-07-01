from django.contrib import messages
from django.shortcuts import render

from Core.forms import AddPlantForm


# Create your views here.


def index(request):
    return render(request, 'home.html')


def add_plant(request):
    if request.method == 'POST':
        form = AddPlantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plant Added Successfully!!!')
        else:
            messages.error(request, 'Invalid Form')
            print(form)
    else:
        form = AddPlantForm()
    context = {
        'form':form
    }
    return render(request, 'add_plant.html' ,context)
