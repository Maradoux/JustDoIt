from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Todo

def create_user_group():
    manager_group = Group.objects.get_or_create(name='Project Managers')
    team_member_group = Group.objects.get_or_create(name= 'Team Members')

    todo_content_type = ContentType.objects.get_for_model(Todo)

    add_todo = Permission.objects.get_or_create(codename='add_todo', name='Can add todo', content_type=todo_content_type)[0]
    change_todo = Permission.objects.get_or_create(codename='change_todo', name='Can change todo', content_type=todo_content_type)[0]
    delete_todo = Permission.objects.get_or_create(codename='delete_todo', name='Can delete todo', content_type=todo_content_type)[0]
    update_todo = Permission.objects.get_or_create(codename='update_todo', name='Can update todo', content_type=todo_content_type)[0]

    manager_group.permissions.add(add_todo, change_todo, delete_todo, update_todo)
    team_member_group.permissions.add(add_todo, change_todo)

    return {
        'managers': manager_group,
        'team_members': team_member_group
    }