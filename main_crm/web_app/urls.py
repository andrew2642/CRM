from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_record/', views.create_record, name='create_record'),
    path('view/<int:record_id>/', views.veiw_record, name='view_record'),
    path('update/<int:record_id>/', views.update_record, name='update_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('search/', views.search, name='search'),
]