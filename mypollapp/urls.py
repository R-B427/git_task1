from django.urls import path
from . import views

app_name = 'mypollapp'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # root URL shows welcome page
    path('polls/', views.index, name='index'),  # main poll index under /polls/
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('bootstrap/', views.bootstrap_page, name='bootstrap'),
]
