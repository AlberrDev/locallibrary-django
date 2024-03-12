from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import datetime
from .forms import *
from django.contrib.auth.decorators import permission_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import render_to_string
import os.path
from django.template.loader import get_template
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.conf import settings
from .email_utils import send_email_with_attachment
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Permission
from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm 

# @login_required
def index(request):

    """
    #Level constant tag
    #       Debug    debug
            INFO     info   
            SUCCESS  success
            WARNING   warning
            ERROR     error

    """ 
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.all().count()
    authors = Author.objects.get(pk=1)

    books=Book.objects.all()
    lista_nombres=['nombre1','nombre2','nombre3']
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    if num_visits % 2 == 0:

    #Manera1 sin el tag
        messages.add_message(request=request,level=messages.INFO,message="Mensaje de uno de INFO")
        #Manera2 con el tag
        messages.info(request,"HOLAAA")
        messages.success(request,"SUCCESS")
        messages.warning(request,"WARNING")
        messages.error(request,"ERROR")
        messages.debug(request,"DEBUG1")

    return render(
        request,
        'index.html',
        context=
        {'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,
         'datos':lista_nombres, 'books':books,'num_visits':num_visits,'authors':authors}
    )

def probando(request,par1):
    book = Book.objects.get(pk=par1)
    
    

    return render(
        request,
        "detail_view.html",context={"book":book}
    )

#Funcion para mediante el id del autor coger el objeto autor

def autores(request,par2):
    author = Author.objects.get(pk=par2)
    

    return render(
        request,
        "detail_view_author.html",context={"author":author}
    )

class Calculator(View):

    def calculator(request,numero = 0,signo = ""):
        lista_num = request.session.get('lista_num')
        resultado=""
        if numero != 0 and signo == "":

            request.session['lista_num'] += str(numero)
        elif signo != "" and numero==0:
            if signo == "suma":
                signo = "+"
            elif signo == "restar":
                signo = "-"
            elif signo == "multi":
                signo = "*"
            elif signo == "div":
                signo = "/"
            elif signo == "borrar":
                signo = ""
                request.session['lista_num'] = ""
            elif signo == "igual":
                resultado = eval(lista_num)
                signo = ""
                request.session['lista_num'] = ""
                print(resultado)

            request.session['lista_num'] += signo
        lista_num = request.session.get('lista_num')




       
        
        return render(
        request,
        "calculator.html",context={'lista_num':lista_num,"resultado"
                                   :resultado}
    )
    
        




from django.views import generic

class BookListView(generic.ListView):
    model = Book
    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'Estos son solo algunos war'
        return context

class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by=1
    def get_queryset(self):
        return Author.objects.filter(first_name__icontains='n')
    
class AuthorDetailView(generic.DetailView):
    model = Author


class BookInstanceListView(generic.ListView):
    model = Book
    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5]

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'Estos son solo algunos war'
        return context



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):

    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class TotalLibrosPrestadosListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):

    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    




@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #Aqui lo que hacemos es sacar el valor del formu y updatear dde la BBDD
            #Ya que en el formu se cambia el valor del due.back
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('prestado') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})



def formularioCompleto(request):

    book = Book.objects.all()

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = FormularioCompleto(request.POST,request.FILES)
        #Importante el request files para que se puedan manejar ficheros y imagenes
   
        print(form.is_valid())
        if form.is_valid():
            print("Cleaned data")
            print(form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('formu'))
    else:
        form = FormularioCompleto()
    # If this is a GET (or any other method) create the default form.

    return render(request, 'catalog/formuCompleto.html', {'form': form, 'book':book})



class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


def formularioExamen(request):

    book = Book.objects.all()

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = FormularioCompleto(request.POST,request.FILES)
        #Importante el request files para que se puedan manejar ficheros y imagenes
        print(form.is_valid())
        if form.is_valid():
            print("Cleaned data")
            print(form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('formu') )
    else:
        form = FormularioCompleto()
    # If this is a GET (or any other method) create the default form.

    return render(request, 'catalog/formuExamen.html', {'form': form, 'book':book})

def generarPdf(request,id):
    # path = 'catalog/media/pdf'
    # dirname = os.path.dirname(path)
    # print(dirname)
    book = Book.objects.get(pk=id)
    print(book)
    template = get_template('catalog/transformar_datos.html')
    context = {'book': book,'portada_url': book.portada.url}
    html = template.render(context)
    pdf_file = HTML(string=html).write_pdf()

    book.ficheros.save(f'{book.title}.pdf', ContentFile(pdf_file), save=True)

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{book.title}.pdf"'
    return response
   
    

def formularioExamen(request):
    if request.method == 'POST':

        form = FormularioExamen(request.POST,request.FILES)
       
        if form.is_valid():
            print("Cleaned data")
            titulo1 = form.cleaned_data["titulo"]
            authorSacar = form.cleaned_data["author"]
            author_pk1 = authorSacar.pk
            summary1 = form.cleaned_data["summary"]
            isbn1 = form.cleaned_data["isbn"]
            genre_sacar = form.cleaned_data["genre"]
            # genre_pk1 = genre_sacar.pk
            portada1 = form.cleaned_data["portada"]
            video1 = form.cleaned_data["video"]
            ficheros1 = form.cleaned_data["ficheros"]
            email = form.cleaned_data["email"]
            #Hago esto ya que al generar el email me paso en el book title y si tiene espacios
            #No encuentra el pdf que se genera con _
            
            if " " in titulo1:
                titulo1 = titulo1.replace(" ", "_")
            print("submit")

            book = Book.objects.create(title=titulo1,summary=summary1,isbn=isbn1,author_id=author_pk1,ficheros="",video=video1,
                                        portada=portada1)
            
            for genre in genre_sacar:
                genre_pk = genre.pk
                print(genre_pk)
                book.genre.add(genre_pk)
            book.save()
            if request.POST.get("genpdf"):
                template = get_template('catalog/transformar_datos.html')
                context = {'book': book}
                html = template.render(context)
                pdf_file = HTML(string=html,base_url=request.build_absolute_uri()).write_pdf()

                book.ficheros.save(f'{book.title}.pdf', ContentFile(pdf_file), save=True)

                response = HttpResponse(pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="{book.title}.pdf"'
                return response
            elif request.POST.get("genemail"):
                template = get_template('catalog/transformar_datos.html')
                context = {'book': book}
                html = template.render(context)
                pdf_file = HTML(string=html,base_url=request.build_absolute_uri()).write_pdf()
                book.ficheros.save(f'{book.title}.pdf', ContentFile(pdf_file), save=True)
                response = HttpResponse(pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="{book.title}.pdf"'  
                subject = f'ListView de tu libro {book.title}'
                message = 'Aqui te adjunto el PDF de tu ListView del libro'
                from_email = f'{email}'  
                recipient_list = [f'{email}']  
                attachment_path = f'catalog/media/pdf/{book.title}.pdf' 
                file_path = settings.BASE_DIR / attachment_path
                send_email_with_attachment(subject, message, from_email, recipient_list, attachment_path)

                return HttpResponse("El email ha sido enviado de locos")                
                
                
            
            else:
                return HttpResponseRedirect(reverse('formuExamen'))
            
    
    else:
        form = FormularioExamen()
    return render(request, 'catalog/formuExamen.html', {'form': form})






def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = form.save()
            login(request,user)
            subject = f'Tu cuenta ha sido creada con exito'
            message = 'Aqui tienes tu creacion GOD'
            from_email = f'{email}'  
            recipient_list = [f'{email}']  
            attachment_path = f'catalog/media/pdf/Bienvenida.pdf' 
            file_path = settings.BASE_DIR / attachment_path
            send_email_with_attachment(subject, message, from_email, recipient_list, attachment_path)
        return redirect('index')  
    else:
        form = UserCreationForm()
    return render(request, 'catalog/register.html', {'form': form})

@permission_required("catalog.permiso2")
def creacion_perfil (request):
    if request.method == 'POST':
        form = CreacionPerfilForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["users"]
            dni = form.cleaned_data["dni"]
            direccion = form.cleaned_data["direccion"]
            provincia = form.cleaned_data["provincia"]
            telefono = form.cleaned_data["telefono"]
            localidad = form.cleaned_data["localidad"]
            mandar_mensajes = form.cleaned_data["mandar_mensajes"]
            recibir_mensajes = form.cleaned_data["recibir_mensajes"]

            user1 = Perfiles.objects.create(user = user,dni=dni,direccion=direccion,provincia=provincia,telefono=telefono,localidad=localidad)
            
            #Aqui lo que hago es en caso de que el boolean sea true recupero el permiso de la tabla Permission
            #Y se lo agrego al objeto user
            if mandar_mensajes == True:
                mandar_permiso = Permission.objects.get(name='Mandar mensajes')
                user.user_permissions.add(mandar_permiso)
            if recibir_mensajes == True:
                recibir_permiso = Permission.objects.get(name='Recibir Mensajes')
                user.user_permissions.add(recibir_permiso)

            user1.save()
            
        return redirect('crear-perfil')
    else:
        form = CreacionPerfilForm()
    
    return render(request, 'catalog/formulario_creacion.html', {'form': form})



@permission_required("catalog.mandar_mensajes")
def mandar_mensajes (request):
    if request.method == "POST":
        form = MandarMensajesForm(request.POST)
        print(form)
        provincia_busqueda = []
        localidad_busqueda = []
        resultado = []
        pks = []
        print(form.cleaned_data)
        provincia_buscar = form.cleaned_data["provincia"]
        localidad_buscar = form.cleaned_data["localidad"]

        if provincia_buscar != "" and localidad_buscar != "":
            datos_generales = Perfiles.objects.filter(provincia=provincia_buscar,localidad=localidad_buscar)

        else:
            if provincia_buscar != "":
                datos_generales = Perfiles.objects.filter(provincia=provincia_buscar)
                print(provincia_busqueda)
                print("arrba")
            if localidad_buscar != "":
                datos_generales = Perfiles.objects.filter(localidad=localidad_buscar)
                print(localidad_busqueda)
      
        
        resultado = list(set(datos_generales)) #Eliminar duplicados y lo convierte en lista
        resultado_pks = [perfil.pk for perfil in resultado] #Cogemos todas las claves primarias de los Perfiles Buscados
        perfiles_filtrados = Perfiles.objects.filter(pk__in=resultado_pks) # Hacemos un filter con ellos
        usuarios = [perfil.user for perfil in perfiles_filtrados] #Usuarios de los perfiles filtrados
        print(usuarios)

      

        return render (
            request,"catalog/mandar_mensajes.html",{"form":form,"users":usuarios}
        )


    else:
        form = MandarMensajesForm()

        return render (
            request,"catalog/mandar_mensajes.html",{"form":form}
        )
    
@permission_required("catalog.mandar_mensajes")
def gestion_mensaje2(request,pk):
    if request.method == "POST":
        
        form = EnvioMensaje(request.POST)
        if form.is_valid():
            usuario_limpio = form.cleaned_data["users"]
            usuario_obtenido = User.objects.get(username=usuario_limpio)
            print(usuario_obtenido)
            nombre_limpio=form.cleaned_data["nombre"]
            destinatario_limpio=form.cleaned_data["destinatario"]
            destinatario_obtenido = User.objects.get(username=destinatario_limpio)
            cuerpo_mensaje_limpio=form.cleaned_data["cuerpo_mensaje"]
            fecha_envio_limpio=form.cleaned_data["fecha_envio"]

            Mensaje = Mensajes.objects.create(user=usuario_obtenido,nombre=nombre_limpio,
                destinatario = destinatario_obtenido, cuerpo_mensaje=cuerpo_mensaje_limpio,
                fecha_envio=fecha_envio_limpio)
            
            Mensaje.save()
        return redirect('crear-mensaje')

          
    else:
        form = EnvioMensaje()
        usuario = User.objects.get(pk=pk)
        current_user = request.user
        form = EnvioMensaje(initial={'users': current_user,'destinatario':usuario})
        
        #Acceder al campo para modificar datos
        # form.fields['destinatario'].queryset = User.objects.filter(pk=pk)
        # form.fields['users'].queryset = current_user
        return render (request,"catalog/envio_mensaje.html",{"form":form})
    



from django.http import JsonResponse 
from django.forms import model_to_dict 
from datetime import datetime

class BookView(View): 

    def get (self,request): 

        libros = Book.objects.all() 

        return JsonResponse (list(libros.values()),safe=False) 

class BookDetailApi(View):  

    def get (self,request,pk): 

        libros = Book.objects.filter(pk=pk) 

        return JsonResponse (list(libros.values()),safe=False) 
    

class MensajesListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.permiso3'
    model = Mensajes
    template_name ='catalog/mensajes_listar.html'
    def get_queryset(self):
        return Mensajes.objects.filter(destinatario=self.request.user,fecha_envio__lte = datetime.now())
    

class AdministrarListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.permiso3'
    model = Mensajes
    template_name ='catalog/mensajes_admin.html'
    def get_queryset(self):
        return Mensajes.objects.filter(fecha_envio__gte = datetime.now())

class MensajesUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.permiso3'
    model = Mensajes
    fields = ['cuerpo_mensaje','fecha_envio']
    success_url = reverse_lazy('administrar_mensajes')

class MensajesDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.permiso3'
    model = Mensajes
    success_url = reverse_lazy('administrar_mensajes')
  

