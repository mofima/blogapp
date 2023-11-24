from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic.edit import UpdateView, DeleteView
from django.views import View 
from django.db.models import Q 

from .models import Article, Comment, Category
from .forms import NewArticleForm, CommentForm

class NewArticle(LoginRequiredMixin, View):
    def get(self, request):
        form = NewArticleForm()
        ctx = {'form': form,
               'title': 'New Article'}
        return render(request, 'item/new.html', ctx)
    
    def post(self, request):
        form = NewArticleForm(request.POST, request.FILES)

        if not form.is_valid():
            ctx = {'form': form,
               'title': 'New Article'}
            return render(request, 'item/new.html', ctx)
        
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        return redirect('item:detail', pk=article.id) # supposed to redirect to article detail
    
class ArticleDetail(View):
    template_name = 'item/detail.html'

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        related_articles = Article.objects.filter(category=article.category).exclude(pk=pk)[0:4]
        comment_form = CommentForm()
        comments = Comment.objects.filter(article=article).order_by('-updated_at')

        context = {
            'article': article, 'related_articles': related_articles,
            'comment_form': comment_form, 'comments': comments
        }

        return render(request, self.template_name, context)
    
class ArticleUpdateView(LoginRequiredMixin, View):
    model = Article
    template = 'item/article_Update_form.html'

    def get(self, request, pk):
        article = get_object_or_404(self.model, pk=pk, author=request.user)
        form = NewArticleForm(instance=article)
        ctx = {'form':form}
        return render(request, self.template, ctx)
    
    def post(self, request, pk):
        article = get_object_or_404(self.model, pk=pk, author=request.user)
        form = NewArticleForm(request.POST, request.FILES, instance=article)

        if not form.is_valid():
            ctx = {'form':form}
            return render(request, self.template, ctx)
        
        form.save()

        return redirect('item:detail', pk=article.id)
    
class ArticleDeleteView(LoginRequiredMixin, View):
    model = Article 
    template = 'item/article_delete.html'

    def get(self, request, pk):
        article = get_object_or_404(self.model, pk=pk, author=request.user)
        form = NewArticleForm(instance=article)
        ctx = {'form':form,
               'article':article}

        return render(request, self.template, ctx)
    
    def post(self, request, pk):
        article = get_object_or_404(self.model, pk=pk, author=request.user)
        article.delete()
        return redirect('core:index')
    

class BrowseView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        category_id = request.GET.get('category', 0)
        categories = Category.objects.all()
        articles = Article.objects.all() 

        if category_id:
            articles = articles.filter(category_id=category_id)

        if query:
            articles = articles.filter(Q(topic__icontains=query) | Q(content__icontains=query))

        ctx = {
            'articles':articles,
            'query':query,
            'categories':categories,
            'category_id':int(category_id),
        }   

        return render(request, 'item/browse.html', ctx) 

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        comment = Comment(text=request.POST['text'], article=article, created_by=request.user)
        comment.save()
        return redirect('item:detail', pk=article.id)

# class CommentDeleteView(LoginRequiredMixin, View):
#     def get(self, request, pk):
#         comment_id = request.Get.get('comment', 0)
#         if comment_id:
#             article = get_object_or_404(Article, pk=article.id)
#             comment = Comment.objects.filter(article=article, comment_id=comment_id)
#             ctx = {
#                 'comment': comment 
#             }


    