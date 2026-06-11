from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView

from team.forms import TeamForm
from team.models import Team, TeamMember
from django.contrib.auth.mixins import LoginRequiredMixin




from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Board, Team, TeamMember
from .forms import BoardForm


# Create your views here.

class TeamListView(LoginRequiredMixin,ListView):
    model = Team
    template_name = "team_list.html"
    context_object_name = "teams"

    def get_queryset(self):
        return Team.objects.filter(
            members__user=self.request.user
        ).distinct().order_by("-created_at")
    

class TeamDetailView(LoginRequiredMixin,DetailView):
    model = Team
    template_name = "team_detail.html"
    context_object_name = "team"

    def get_object(self):
        team = get_object_or_404(Team,id=self.kwargs['pk'])

        if not TeamMember.objects.filter(team=team,user=self.request.user).exists():
            raise PermissionDenied("You are not a member of this team.")
        return team




class TeamCreateView(LoginRequiredMixin,CreateView):
    model = Team
    template_name = "team_create.html"
    form_class = TeamForm
    success_url = reverse_lazy("team-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        TeamMember.objects.create(
            team=self.object,
            user=self.request.user,
            role='admin',
        )
        return response
    

    
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from .models import Board, TeamMember
    
class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = "board_detail.html"
    context_object_name = "board"

    def get_queryset(self):
        return Board.objects.prefetch_related(
            'columns',
            'columns__tasks'
        )

    def get_object(self, queryset=None):
        board = super().get_object(queryset)

        if not TeamMember.objects.filter(
            team=board.team,
            user=self.request.user
        ).exists():
            raise PermissionDenied("You do not have access to this board.")

        return board
    
from django.views.generic import CreateView
from django.shortcuts import redirect
from .models import Column, Task
from .forms import TaskCreateForm

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Fetch the column first to find out which team this belongs to
        column = get_object_or_404(Column, id=self.kwargs['column_id'])
        # Pass the team context to the form filtering logic we wrote above
        kwargs['team'] = column.board.team
        return kwargs
    
    

    def form_valid(self, form):
        column = get_object_or_404(Column, id=self.kwargs['column_id'])
        
        # Security: Double check that the user actually belongs to this team
        if not column.board.team.members.filter(user=self.request.user).exists():
            raise PermissionDenied("You cannot add tasks to this workspace.")
        
        # Manually bind the column to the task instance before saving
        form.instance.column = column
        form.save()
        
        # Redirect right back to the board detail view
        return redirect('board-detail', pk=column.board.id)
    






class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    form_class = BoardForm
    template_name = "board_create.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Runs before GET and POST requests.
        Fetch the team and verify that the user belongs to it.
        """
        self.team = get_object_or_404(
            Team,
            id=self.kwargs["team_id"]
        )

        # Permission check
        if not TeamMember.objects.filter(
            team=self.team,
            user=request.user
        ).exists():
            raise PermissionDenied(
                "You cannot create boards in this team."
            )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Pass the team to the template so we can show
        information like the team name and cancel link.
        """
        context = super().get_context_data(**kwargs)
        context["team"] = self.team
        return context

    def form_valid(self, form):
        """
        Automatically attach the board to the team.
        """
        form.instance.team = self.team

        response = super().form_valid(form)

        return response

    def get_success_url(self):
        """
        After creating the board, return to the Team Detail page.
        """
        return reverse_lazy(
            "team-detail",
            kwargs={"pk": self.team.id}
        )
    


