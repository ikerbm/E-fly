from datetime import date
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.widgets import DateInput, Select
from django.forms.widgets import SelectDateWidget
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class DateInput(SelectDateWidget):
    def __init__(self, *args, **kwargs):
        # establece el rango de años disponibles
        current_year = date.today().year
        years = range(current_year-18, current_year-100, -1)
        kwargs['years'] = years
        super().__init__(*args, **kwargs)

class CardDateInput(SelectDateWidget):
    def __init__(self, *args, **kwargs):
        # establece el rango de años disponibles
        current_year = date.today().year
        years = range(current_year, current_year+10, -1)
        kwargs['years'] = years
        super().__init__(*args, **kwargs)


class CreateUsuarioForm(UserCreationForm):
    fechaNaci = forms.DateField(widget=DateInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if ' ' in password1:
            raise forms.ValidationError('La contraseña no puede contener espacios en blanco.')
        return password1
    def clean_fechaNaci(self):
        fechaNaci = self.cleaned_data.get('fechaNaci')
        today = date.today()
        age = today.year - fechaNaci.year - ((today.month, today.day) < (fechaNaci.month, fechaNaci.day))
        if age < 18:
            raise forms.ValidationError('Debes tener al menos 18 años para registrarte.')
        return fechaNaci
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email',
                  'DNI','fechaNaci',
                  'lugarNaci','dirFact','sexo','tipoUsuario'] 
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'lugarNaci': forms.TextInput(attrs={'class': 'form-control'}),
            'dirFact': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'DNI': forms.NumberInput(attrs={'class': 'form-control'}),
        }
                  
class CreateAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email',
                  'DNI','tipoUsuario'] 
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'DNI': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model=User

class EditForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name',
                'lugarNaci','dirFact','sexo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'lugarNaci': forms.TextInput(attrs={'class': 'form-control'}),
            'dirFact': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
        }

class AddCardForm(forms.ModelForm):

    '''
    arreglar fecha del mes actual, hasta 10 años, esta aceptando tarjetas vencidas
    y necesitamos que no solicite el dia, solo mes y año
    '''

    vencimiento = forms.DateField(widget=CardDateInput)

    def clean_vencimiento(self):
        vencimiento = self.cleaned_data.get('vencimiento')
        today = date.today()
        if vencimiento < today:
            raise forms.ValidationError('La tarjeta está vencida.')
        return vencimiento
    
    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if len(numero) != 16:
            raise forms.ValidationError('El número de tarjeta debe tener 16 dígitos.')
        return numero

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if len(cvv) != 3:
            raise forms.ValidationError('El CVV debe tener 3 dígitos.')
        return cvv
    
    class Meta:
        model = Tarjeta
        fields = ['tipo','numero','nombre','cvv','vencimiento'] 
        
    widgets = {
            'cvv': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),            
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),            
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

