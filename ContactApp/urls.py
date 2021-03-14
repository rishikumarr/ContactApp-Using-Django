from django.urls import path
from ContactApp import views
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('register/',views.RegisterPage.as_view(),name='register'),
    path('login/',views.CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('',views.index,name='index'),
    path('view-contact/<str:pk>',views.viewContact,name='view-contact'),
    path('edit-contact/<str:pk>',views.editContact,name='edit-contact'),
    path('add-contact/',views.addContact,name='add-contact'),
    path('delete-contact/<str:pk>',views.deleteContact,name='delete-contact'),
    path('settings/',views.settings,name='settings'),
    path('export_csv',views.export_csv,name='export_csv'),
]