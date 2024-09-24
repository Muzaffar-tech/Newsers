from tkinter.font import names

from django.urls import path

from .views import index, detail, register, user_login, user_logout, change_news, save_comment

urlpatterns = [
    path('', index, name='home'),
    path('detail/<int:pk>', detail, name='detail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('change/', change_news, name='change'),
    path("save-comment/<int:news_id>/", save_comment, name='add_comment')
]
