from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todolist/<int:page>/', views.todolist, name='todolist'),
    path('createTodo/', views.create_todo, name='createTodo'),
    path('doneTodo/', views.done_todo, name='doneTodo'),
    path('deleteTodo/', views.delete_todo, name='deleteTodo'),
    path('editTodo/', views.edit_todo, name='editTodo')
]
