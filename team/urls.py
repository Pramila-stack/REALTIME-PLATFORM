from django.urls import path

from team import views

urlpatterns = [
    path("",views.TeamListView.as_view(),name="team-list"),
    path("team-detail/<int:pk>/",views.TeamDetailView.as_view(),name="team-detail"),
    path("team-create/",views.TeamCreateView.as_view(),name="team-create"),
    path('boards/<int:pk>/', views.BoardDetailView.as_view(), name='board-detail'),
    path('columns/<int:column_id>/add-task/', views.TaskCreateView.as_view(), name='task-create'),
    path(
    "team/<int:team_id>/board/create/",
    views.BoardCreateView.as_view(),
    name="board-create",
),
]