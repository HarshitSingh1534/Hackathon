from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page,name='homepage'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_hackathon/', views.create_hackathon, name='create_hackathon'),
    path('hackathons/', views.all_hackathons, name='all_hackathons'),
    path('hackathons/<int:hackathon_id>/', views.hackathon_detail, name='hackathon_detail'),
    path('hackathons/<int:hackathon_id>/register/', views.register_for_hackathon, name='register_for_hackathon'),
    path('hackathons/<int:hackathon_id>/submissions/', views.submit_to_hackathon, name='submit_to_hackathon'),
    path('my_hackathons/', views.my_hackathons, name='my_hackathons'),
]
