from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Todo, Notification

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'justdoit/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(models.Q(created_by= self.request.user) | models.Q(assigned_to= self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications'] = Notification.objects.filter(user = self.request.user, is_read=False)
        return context
    
class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'justdoit/todo_detail.html'

class TodoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'due_date', 'priority', 'assigned_to']
    template_name = 'justdoit/todo_create.html'
    permission_required = 'justdoit.add_todo'
    success_url = reverse_lazy('todo_list.html')

    def form_invalid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class TodoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description','status', 'due_date', 'priority', 'assigned_to', 'completed']
    template_name = 'justdoit/todo_update.html'
    permission_required = 'justdoit.change_todo'
    success_url = reverse_lazy('todo_list')

        
    