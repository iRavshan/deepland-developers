from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/project_form.html'
    fields = ['title', 'description', 'image', 'github_link', 'live_link', 'authors']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # By default select the current user
        form.initial['authors'] = [self.request.user.pk]
        return form
        
    def form_valid(self, form):
        response = super().form_valid(form)
        # Ensure the creator is in the authors list
        self.object.authors.add(self.request.user)
        return response
