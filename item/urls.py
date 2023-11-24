from django.urls import path, reverse_lazy 

from . import views 

app_name = 'item'
urlpatterns = [
    path('', views.BrowseView.as_view(), name='browse'),
    path('new/', views.NewArticle.as_view(), name='new'),
    path('<int:pk>/', views.ArticleDetail.as_view(), name='detail'),
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='delete'),
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    # path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url=reverse_lazy('core:index')), name='comment_delete')
]