from django.urls import path 
from django.urls import re_path 
from . import views 
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from django.conf.urls.static import static
 

urlpatterns = [ 

    path('',views.index,name='index'), 
    path('index/',views.index,name='index'), 
    path("probando/<int:par1>",views.probando,name="probando"),
    path("autores/<int:par2>",views.autores,name="autores"),
    path('books/', views.BookListView.as_view(), name='books'),
    path('author/', views.AuthorListView.as_view(), name='author'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('calculator/', views.Calculator.calculator, name='calculator'),
    path('calculator/<int:numero>', views.Calculator.calculator, name='calculator'),
    path('calculator/<str:signo>', views.Calculator.calculator, name='calculator'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('prestado/', views.TotalLibrosPrestadosListView.as_view(), name='prestado'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('formu/', views.formularioCompleto, name='formu'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('formuExamen/', views.formularioExamen, name='formuExamen'),
    path('generarPDF/<int:id>', views.generarPdf, name='generarPDF'),
    path('register', views.register, name='register'),
    path('crear-perfil', views.creacion_perfil, name='crear-perfil'),
    path('crear-mensaje', views.mandar_mensajes, name='crear-mensaje'),
    path('bookAPI', views.BookView.as_view(), name='bookAPI'), 
    path('bookDetailApi/<int:pk>', views.BookDetailApi.as_view(), name='bookDetailApi'), 
    path('gestion_mensaje/<int:pk>', views.gestion_mensaje2, name='gestion_mensaje'), 
    path('mensajes_list', views.MensajesListView.as_view(), name='mensajes_list'),
    path('administrar_mensajes', views.AdministrarListView.as_view(), name='administrar_mensajes'), 
    path('mensajes/<int:pk>/update/', views.MensajesUpdate.as_view(), name='mensajes-update'),
    path('mensajes/<int:pk>/delete/', views.MensajesDelete.as_view(), name='mensajes-delete'),


    # re_path(r'^$',login_required(views.index),name='index')


] 

