from django import forms
from capitulos.models import ExercicioUsuario


class ExercicioUsuarioNotaForm(forms.ModelForm):
    class Meta:
        model = ExercicioUsuario
        fields = ['dificuldade']
        widgets = {
            'dificuldade': forms.RadioSelect(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dificuldade'].required = True