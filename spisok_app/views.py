from django.shortcuts import render, redirect
from .forms import NameForm
from .models import NameEntry

def index(request):
    names_list = NameEntry.objects.all()
    
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            
            # Определяем следующий порядковый номер
            last_entry = NameEntry.objects.order_by('-order_number').first()
            next_number = last_entry.order_number + 1 if last_entry else 1
            
            # Сохраняем новое имя
            NameEntry.objects.create(
                name=name,
                order_number=next_number
            )
            
            return redirect('index')
    else:
        form = NameForm()
    
    return render(request, 'index.html', {
        'form': form,
        'names_list': names_list
    })