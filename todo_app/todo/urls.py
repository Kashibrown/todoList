from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [ 
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='todo/registration/password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='todo/registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='todo/registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='todo/registration/password_reset_complete.html'),name='password_reset_complete'),            
               
    path('register/', Register.as_view(), name='register'),
    path('login/', myLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    
    path('', Home, name='home'),
    path('list/', TodoList.as_view(), name='list'),
    path('task-create/', TodoCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TodoUpdate.as_view(), name='task-update'),
    path('task-detail/<int:pk>/', TodoDetail.as_view(), name='task-detail'),
    path('task-delete/<int:pk>/', TodoDelete.as_view(), name='task-delete'),
]
