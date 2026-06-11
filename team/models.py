from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('admin','Admin'),
        ('member','Member'),
    ]
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="members")
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    role = models.CharField(max_length=200,choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.team.name} - {self.user.username}'
    


class Board(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="boards")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} - {self.team.name}'
    

class Column(models.Model):
    # Added related_name="columns"
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=50)
    order = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.board.name}'

class Task(models.Model):
    # Added related_name="tasks"
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.column.name}'


class ChatMessage(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} - {self.message}'

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.message}'

class ActivityLog(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.team.name} - {self.action}'

class TaskFile(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    file = models.FileField(upload_to="task_files/")
    uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.task.title