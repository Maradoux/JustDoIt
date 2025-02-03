from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        fields = UserCreationForm.Meta.fields + ('email',)

class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Automatically add new user to Team Members group
        team_member_group = Group.objects.get(name='Team Members')
        self.object.groups.add(team_member_group)
        return response

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'login'