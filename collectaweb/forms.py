from django import forms
#from django.contrib.auth.models import User
from users.models import User
class RegisterForm(forms.Form):
    username = forms.CharField(required=True,label = 'Usuario', min_length=4, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'id': 'username',
                                    'placeholder': 'Nombre de usuario'
                                }))
    first_name = forms.CharField(required=True, label = 'Nombre',min_length=4, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'id': 'first_name',
                                    'placeholder': 'Nombre'
                                }))
    last_name = forms.CharField(required=True, label = 'Apellidos',min_length=4, max_length=50,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'id': 'last_name',
                                    'placeholder': 'Apellidos'
                                }))
    email =  forms.EmailField(required=True,  label = 'Correo',widget=forms.EmailInput(attrs={
                                    'class': 'form-control',
                                    'id': 'email',
                                    'placeholder': 'Email'}))
    password = forms.CharField(required=True,label = 'Contraseña',  widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'id': 'password',
                                    'placeholder': 'Contraseña'}))
    password2 = forms.CharField(required=True,  label = 'Confirmar contraseña', widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'id': 'password2',
                                    'placeholder': 'Repite la contraseña'}))


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya se encuentra en uso')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo {} ya se encuentra en uso'.format(email))
        
        return email 

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'La contraseña no coincide')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )