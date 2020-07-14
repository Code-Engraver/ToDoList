from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from urllib.parse import urlparse
from .models import Todo

from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import re


class Index(RedirectView):

    pattern_name = 'todolist'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(page=1, *args, **kwargs)


class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            return 1.1


class TodoList(ListView):
    template_name = "my_to_do_app/index.html"
    model = Todo
    paginator_class = SafePaginator
    paginate_by = 5
    queryset = Todo.objects.all().order_by("-id")

    def get(self, request, *args, **kwargs):
        context = super(TodoList, self).get(request, *args, **kwargs)
        paginator = context.context_data.get('paginator')

        page = str(context.context_data.get('page_obj'))

        if not page.find(".") == -1:
            return HttpResponseRedirect(reverse('index'))

        page = int(re.sub(r"\D", "", page.split("of")[0]))
        start_page = 1 if page - 4 <= 0 else page - 4
        end_page = paginator.num_pages if page + 4 > paginator.num_pages else page + 4
        paginator_range = range(start_page, end_page + 1)

        context.context_data['paginator_range'] = paginator_range

        return context


class CreateTodo(CreateView):
    model = Todo
    fields = ['content']
    success_url = "/todolist/1/"


class DoneTodo(UpdateView):
    model = Todo
    fields = ['is_done']

    def dispatch(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.is_done = not todo.is_done
        todo.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return f'/todolist/{urlparse(self.request.META.get("HTTP_REFERER")).path.split("/")[2]}'


class DeleteTodo(DeleteView):
    model = Todo

    def get_success_url(self):
        return f'/todolist/{urlparse(self.request.META.get("HTTP_REFERER")).path.split("/")[2]}'


class EditTodo(UpdateView):
    model = Todo
    fields = ['content']

    def get_success_url(self):
        return f'/todolist/{urlparse(self.request.META.get("HTTP_REFERER")).path.split("/")[2]}'
