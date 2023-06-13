from django.shortcuts import render, redirect 
from django.views.generic import FormView, ListView, CreateView, DetailView, DeleteView, UpdateView
from .form import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import *

#this is for the password reset
from django.contrib.auth.tokens import default_token_generator 


class Register(FormView):
    form_class = RegisterForm
    template_name = "todo/register.html"
    success_url = reverse_lazy("login") 
    redirect_authenticated_user= True
    
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list')     
        return super(Register,self).get(*args, **kwargs)
            
    
class myLogin(LoginView):
    template_name = 'todo/login.html'
    redirect_authenticated_user = True
    fields = "__all__"
    
    def get_success_url(self):
        return reverse_lazy('list')
    

class TodoCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "todo/create.html"
    fields = ['title','content','complete']
    success_url = reverse_lazy('list') 
    
    def form_valid(self, form): #this method would save the user form to the logged in user.
        form.instance.user = self.request.user 
        return super(TodoCreate, self).form_valid(form) 
    
    

def Home(request):
    return render(request, 'todo/home.html')
    
class TodoList(ListView):
    template_name = "todo/list.html"
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs): #this is useful so other users would not be able to see the logged in user todo lists.
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count 
        
        search_bar = self.request.GET.get('search-bar') or ''
        if search_bar:
            context['tasks'] = context['tasks'].filter(title__startswith = search_bar)
        context['search_bar'] = search_bar        
        
        return context    
    
class TodoDetail(DetailView):
    context_object_name= 'task'
    template_name = 'todo/detail.html'
    model = Task 
    
class TodoDelete(DeleteView):
    model = Task
    context_object_name = 'delete'
    template_name = 'todo/delete.html'
    success_url = reverse_lazy('list')
    
class TodoUpdate(UpdateView):
    model = Task
    template_name = "todo/update.html"
    fields = ['title','content','complete']
    success_url = reverse_lazy('list') 


        
        
#PASSWORD RESET CLASS BASED VIEWS

class PasswordContextMixin:
    extra_context = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title':self.title,
            **(self.extra_context or {})
        })
        return context
    

class PasswordResetView(PasswordContextMixin, FormView):
    token_generator = default_token_generator 
    title = ('Password reset')
    from_mail = 'kashibrwn@gmail.com'
    
    
    