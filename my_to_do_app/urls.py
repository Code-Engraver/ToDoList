from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('todolist/<int:page>/', views.TodoList.as_view(), name='todolist'),
    path('createTodo/', views.CreateTodo.as_view(), name='createTodo'),
    path('doneTodo/<int:pk>/', views.DoneTodo.as_view(), name='doneTodo'),
    path('deleteTodo/<int:pk>/', views.DeleteTodo.as_view(), name='deleteTodo'),
    path('editTodo/<int:pk>/', views.EditTodo.as_view(), name='editTodo')
]
