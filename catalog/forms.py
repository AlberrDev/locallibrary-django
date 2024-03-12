from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.
from django.forms import ModelForm
from .models import *
from django.core.validators import FileExtensionValidator 
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm 

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}),help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
    
class FormularioCompleto(forms.Form):
    LISTA_MASCOTAS =( 
        ("Perro", "Perro"), 
        ("Gato", "Gato"), 
        ("Camaleon", "Camaleon"), 
        ("Avispa", "Avispa"), 
    ) 
    LISTA_OCIOS=(
        ("Cine", "Cine"), 
        ("Gym", "Gym"), 
        ("Programar", "Programar"), 
        ("Cantar", "Cantar"),
    )
    LISTA_SEXO=(
        ("Hombre", "Hombre"), 
        ("Mujer", "Mujer"), 
        ("NULO", "NULO"), 
    )
    COLORES = ( 
    ("Azul", "Azul"), 
    ("Rojo", "Rojo"), 
    ("Verde", "Verde"), 
    ("Amarillo", "Amarillo"), 
    ("Rosa", "Rosa"), 
 ) 

    

    nombre = forms.CharField( max_length=30)
    apellido = forms.CharField(max_length=40)
    edad = forms.DecimalField(decimal_places=0)
    Mascota = forms.MultipleChoiceField (choices = LISTA_MASCOTAS)
    ocio=forms.MultipleChoiceField(choices=LISTA_OCIOS, widget=forms.CheckboxSelectMultiple())
    sexo = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=LISTA_SEXO, 
    )
    hora = forms.TimeField(widget=forms.DateInput(attrs={"type":"time"}))
    colores = forms.ChoiceField(choices=COLORES)
    date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}),help_text="Enter a date between now and 4 weeks (default 3).")
    libro = forms.ModelChoiceField(queryset=Book.objects.all())
    imagen = forms.ImageField()
    Observacion = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))


# class FormularioExamen(forms.Form):
#     titulo = forms.CharField(max_length=200)
#     author = forms.ModelChoiceField(queryset=Author.objects.all())
#     summary = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
#     isbn = forms.CharField(max_length=13)
#     genre = forms.ModelChoiceField(queryset=Genre.objects.all())
#     portada = forms.ImageField()
#     video = forms.FileField()
#     ficheros = forms.FileField() 
#     email = forms.CharField()
 




class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       #Check date is not in past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       #Check date is in range librarian allowed to change (+4 weeks)
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data
    
    class Meta:
        model = BookInstance
        fields = ['due_back',]
        labels = { 'due_back': _('Renewal date'), }
        help_texts = { 'due_back': _('Enter a date between now and 4 weeks (default 3).'), }

class FormularioExamen(forms.Form):
    titulo = forms.CharField(max_length=200)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    summary = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    isbn = forms.CharField(max_length=13)
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.SelectMultiple,required=True)
    portada = forms.ImageField()
    video = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    ficheros = forms.FileField()
    email = forms.EmailField()


#Aqui heredo de UserCreationForm donde incluye la password y usuario donde 
#Hashea la pass y agrego el campo email para enviarle un email
class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email',]

class CreacionPerfilForm(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.all())
    dni = forms.CharField(max_length=200)
    direccion = forms.CharField(max_length=50)
    localidad = forms.CharField(max_length=40)
    provincia = forms.CharField(max_length=40)
    telefono = forms.CharField(max_length=40)
    mandar_mensajes = forms.BooleanField(required=False)
    recibir_mensajes = forms.BooleanField(required=False)

class MandarMensajesForm(forms.Form):
    provincia = forms.CharField(max_length=40 ,required=False)
    localidad = forms.CharField(max_length=40, required=False)


class EnvioMensaje(forms.Form):
  
    users = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    nombre = forms.CharField(max_length=80)
    destinatario = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    cuerpo_mensaje = forms.CharField(max_length=300,widget=forms.Textarea(attrs={"rows":"5"}))
    fecha_envio = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}),help_text="Fecha de Envio")





 


