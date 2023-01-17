from django.urls import path, include
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),

    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    path('resultsdata/<int:pk>/', views.result_data, name='resultsdata'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('<int:pk>/edit/', views.edit_poll_view, name='edit'),

    path('create/', views.create_polls_form_view, name='create'),

    path('<int:pk>/delete/', views.delete_poll_view, name='delete'),

    path('<int:pk>/like/', views.like_view, name='like_poll'),

    path('<int:pk>/add_comment/', views.AddCommentView.as_view(), name='add_comment'),

    path('<int:pk>/edit_comment/', views.EditCommentView.as_view(), name='edit_comment'),
]
