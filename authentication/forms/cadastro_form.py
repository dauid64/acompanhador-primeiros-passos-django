from django import forms
from django.contrib.auth.models import User

class CadastroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de usuário',
            'email': 'Email',
            'password': 'Senha',
        }
    
    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email já cadastrado.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Usuário já cadastrado.")
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'class': 'form-control'}),
        label='Nome de usuário',
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control'}),
        label='Senha',
        required=True
    )
