from django.conf.urls import url

from django.urls import path

from . import views # import views so we can use them in urls.

app_name='catalogue'

urlpatterns = [
    path('', views.listing, name='listing'),
    path('join/', views.join, name='join'),
    path('connexion/', views.connexion, name='connexion'),
    path('user/', views.user, name='user'),
    path('aliment/', views.aliment, name='aliment'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('search/', views.search, name='search'),
    path('<product_id>/', views.detail, name='detail'),
]