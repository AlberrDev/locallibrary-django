from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Requerida para las instancias de libros únicos
# Create your models here.
from django.contrib.auth.models import User 
from datetime import date

from django.core.validators import FileExtensionValidator 


 
class usu(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    comentario= models.TextField(max_length=200) 

class Person(models.Model): 
    first_name = models.CharField(max_length=150) 
    last_name = models.CharField(max_length=150) 
    age = models.IntegerField() 

class Genre(models.Model):

    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
     
        return self.name
    



class Book(models.Model):
 

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")

    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.
    
    portada = models.ImageField(upload_to='catalog/media/imagenes/' ,null=True)

    video = models.FileField(upload_to='catalog/media/videos/',null=True,validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])

    ficheros = models.FileField(upload_to="catalog/media/pdf/" , null=True)


    def __str__(self):
        
        return self.title

    #Devuelve una URL a una instancia particular de book
    def get_absolute_url(self):
        #Reverse es parecido a un join que lo hace mediante el urls y el args
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
  
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre' 




class BookInstance(models.Model):
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank = True)

    class Meta:
        ordering = ["due_back"]
#Nombre de permiso y descripcion
        permissions = (("can_mark_returned", "Set book as returned"),
                       ("can_generate_pdf", "Generate PDF"),
                       ("permiso1","Crear Usuario"),
                       ("permiso2","Crear Perfil Usuario"),
                       ("permiso3","Gestion Mensajes"))
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
      
        return '%s (%s)' % (self.id,self.book.title)
    
class Author(models.Model):
  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
      
        return reverse('author-detail', args=[str(self.id)])

 
    def __str__(self):
       
        return '%s, %s' % (self.last_name, self.first_name)
    
class Perfiles(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    dni = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50, null=True)
    provincia = models.CharField(max_length=40)
    telefono = models.CharField(max_length=40)
    class Meta:
        permissions = (("mandar_mensajes", "Mandar mensajes"),
                       ("recibir_mensajes", "Recibir Mensajes"))
        
class Mensajes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    destinatario = models.ForeignKey(User,on_delete=models.CASCADE, related_name="destinatario")
    cuerpo_mensaje = models.CharField(max_length=50)
    fecha_envio = models.DateField(null=True, blank=True)
    
        

    




