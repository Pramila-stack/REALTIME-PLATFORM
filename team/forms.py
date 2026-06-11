from django.contrib.auth.models import User
from django import forms

from team.models import Team
from django import forms
from .models import Board

# Forms.py here.

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


from django import forms
from .models import Task, TeamMember

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describe this task...'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *file, **kwargs):
        # We pass the team into the form initialization so we can restrict 
        # the "assigned_to" dropdown to ONLY team members.
        team = kwargs.pop('team', None)
        super().__init__(*file, **kwargs)
        if team:
            self.fields['assigned_to'].queryset = User.objects.filter(id__in=team.members.values_list('user_id', flat=True))




class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name"]