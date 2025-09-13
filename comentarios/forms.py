from django import forms

from comentarios.models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['body', 'exercicio']
        labels = {
            'body': 'Comentário:'
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Escreva seu comentário aqui...'
            }),
            'exercicio': forms.HiddenInput()
        }