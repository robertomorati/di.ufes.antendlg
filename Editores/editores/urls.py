from django.conf.urls import patterns, include, url
from django.contrib import admin
from editores.views import IndexView, logout_page
from editores.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
from editores.views import LoginView, LoginCreateView, AutorGetJsonView

from rest_framework import viewsets, routers
from editor_objetos.models import Autor

#from core.viewsset import MyRESTView
admin.autodiscover()


#rest framework
router = routers.DefaultRouter()
#router.register(r'users', Autor)

urlpatterns = patterns('',

     # this URL passes resource_id in **kw to MyRESTView
     #url(r'^api/v1.0/resource/(?P<resource_id>\d+)[/]?$', login_required(MyRESTView.as_view()), name='my_rest_view'),
     #url(r'^api/v1.0/resource[/]?$', login_required(MyRESTView.as_view()), name='my_rest_view'),
    
     # Login / logout.
     url(r"^autendlg/login/$",LoginView.as_view(), name="login",),
     url(r"^autendlg/registrar/$",LoginCreateView.as_view(), name="registrar_create_view",),
     url(r'^autendlg/logout/$', logout_page, name="logout",),
    
    #Dados Autor
    url(r'^autor/get_url_icone/(?P<pk>\w+)/$', AutorGetJsonView.as_view(), name='avatar_autor_get_json_url_view'),
    
    #Pages project
    url(r'^autendlg/', login_required(IndexView.as_view()), name="index"),
    url(r'^editor_objetos/', include('editor_objetos.urls')),
    url(r'^editor_enredos/', include('editor_enredos.urls')),
    url(r'^editor_missoes/', include('editor_missoes.urls')),
    url(r'^editor_movimentos/', include('editor_movimentos.urls')),
    url(r'^editor_jogadores/', include('editor_jogadores.urls')),
   
    
    # Serve static content.
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    
    # Admin django
    url(r'^admin/', include(admin.site.urls)),
    
    

    
    url(r'^', include(router.urls)),
    url(r'^auth_services/', include('rest_framework.urls', namespace='rest_framework')),
    
    
    
    
    #Sem Uso
    #url(r'^autendlg/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^login/$', Login.as_view(), name='login'), 
    #url(r'^autendlg/$', logout_page),
    #url(r'^autendlg/login/$', 'django.contrib.auth.views.login', name='login'),
    #url(r'^login/$', login_user), 

)