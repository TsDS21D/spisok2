from django import forms

class NameForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Введите имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя здесь',
            'style': 'width: 300px; padding: 10px; font-size: 16px;'
        })
    )