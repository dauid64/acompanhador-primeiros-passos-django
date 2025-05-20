from django import forms
from capitulos.models import ExercicioUsuario


class ExercicioUsuarioDificuldadeForm(forms.ModelForm):
    class Meta:
        model = ExercicioUsuario
        fields = ['dificuldade']
        widgets = {
            'dificuldade': forms.RadioSelect(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dificuldade'].required = True

class ExercicioUsuarioNotaForm(forms.ModelForm):
    class Meta:
        model = ExercicioUsuario
        fields = ['nota']
        widgets = {
            'nota': forms.RadioSelect(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nota'].required = True