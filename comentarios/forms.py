from django import forms
from comentarios.models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['body', 'exercicio', 'parent']   # adiciona parent
        labels = {
            'body': 'Comentário:'
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Escreva seu comentário aqui...'
            }),
            'exercicio': forms.HiddenInput(),
            'parent': forms.HiddenInput(),  # novo
        }
