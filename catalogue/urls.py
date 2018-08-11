from django.conf.urls import url

from django.urls import path

from . import views

app_name = 'catalogue'

urlpatterns = [
	path('index/', views.index, name='index'),
    path('catalogue/', views.listing, name='listing'),
    path('join/', views.join, name='join'),
    path('connexion/', views.connexion, name='connexion'),
    path('user/', views.user, name='user'),
    path('aliment/', views.aliment, name='aliment'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('legal_mention/', views.legal_mention, name='legal_mention'),
    path('search/', views.search, name='search'),
    path('<product_id>/', views.detail, name='detail'),
]
