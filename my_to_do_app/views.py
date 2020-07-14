from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from urllib.parse import urlparse
from .models import Todo


def index(request):
    return HttpResponseRedirect(reverse('todolist', args=(1,)))


def todolist(request, page=1):
    paginator = Paginator(Todo.objects.all(), 5)
    page_todo_list = paginator.get_page(page)

    if page > paginator.num_pages:
        return HttpResponseRedirect(reverse('index'))

    start_page = 1 if page - 4 <= 0 else page - 4
    end_page = paginator.num_pages if page + 4 > paginator.num_pages else page + 4

    paginator_range = range(start_page, end_page + 1)

    content = {
        "todo_list": page_todo_list,
        "paginator_range": paginator_range
    }
    return render(request, 'my_to_do_app/index.html', content)


def create_todo(request):
    input_content = request.POST['content']
    new_todo = Todo(content=input_content)
    new_todo.save()
    return HttpResponseRedirect(reverse('todolist', args=(1,)))


def done_todo(request):
    page = urlparse(request.META.get("HTTP_REFERER")).path.split('/')[2]
    input_id = int(request.POST['id'])
    todo = Todo.objects.get(pk=input_id)
    todo.is_done = not todo.is_done
    todo.save()
    return HttpResponseRedirect(reverse('todolist', args=(page,)))


def delete_todo(request):
    page = urlparse(request.META.get("HTTP_REFERER")).path.split('/')[2]
    delete_todo_id = int(request.POST['id'])
    todo = Todo.objects.get(id=delete_todo_id)
    todo.delete()
    return HttpResponseRedirect(reverse('todolist', args=(page,)))


def edit_todo(request):
    page = urlparse(request.META.get("HTTP_REFERER")).path.split('/')[2]
    update_todo_id = int(request.POST['id'])
    input_content = request.POST['content']
    todo = Todo.objects.get(id=update_todo_id)
    todo.content = input_content
    todo.save()
    return HttpResponseRedirect(reverse('todolist', args=(page,)))
