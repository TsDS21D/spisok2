from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import NameForm
from .models import NameEntry
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def index(request):
    names_list = NameEntry.objects.all().order_by('order_number')
    
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            
            # Определяем следующий порядковый номер
            last_entry = NameEntry.objects.order_by('-order_number').first()
            next_number = last_entry.order_number + 1 if last_entry else 1
            
            # Сохраняем новое имя
            new_entry = NameEntry.objects.create(
                name=name,
                order_number=next_number
            )
            
            # Отправляем WebSocket сообщение о новом имени
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'names_updates',
                {
                    'type': 'names_update',
                    'names': get_names_list()
                }
            )
            
            # Если это AJAX запрос, возвращаем JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'name': name,
                    'order_number': next_number
                })
            
            return redirect('index')
    else:
        form = NameForm()
    
    return render(request, 'index.html', {
        'form': form,
        'names_list': names_list
    })

def get_names_list():
    """Вспомогательная функция для получения списка имен"""
    names = NameEntry.objects.all().order_by('order_number')
    return [
        {
            'id': name.id,
            'order_number': name.order_number,
            'name': name.name,
            'created_at': name.created_at.isoformat()
        }
        for name in names
    ]