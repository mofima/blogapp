from django.shortcuts import render, redirect 
from django.views import View 

from item.models import Category, Article
from .forms import SignupForm

def index(request):
    articles = Article.objects.all().order_by('-created_at')[0:6]
    categories = Category.objects.all()
    ctx = {'articles': articles,
           'categories': categories}
    return render(request, 'core/index.html', ctx)

class SignupView(View):
    template = 'core/signup.html'

    def get(self, request):
        form = SignupForm()
        ctx = {'form': form}

        return render(request, self.template, ctx)
    
    def post(self, request):
        form = SignupForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)
        
        form.save()
        return redirect('/login/')

