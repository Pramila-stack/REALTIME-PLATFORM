from asyncio import Task

from django.contrib import admin

from team.models import ActivityLog, Board, ChatMessage, Column, Notification, TaskFile, Team, TeamMember,Task

# Register your models here.
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Task)
admin.site.register(ChatMessage)
admin.site.register(Notification)
admin.site.register(ActivityLog)
admin.site.register(TaskFile)