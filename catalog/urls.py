from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('whiskies/', views.WhiskyListView.as_view(), name='whiskies'),
    path('whisky/create/', views.WhiskyCreate.as_view(), name='whisky-create'),
    path('whisky/<str:pk>', views.WhiskyDetailView.as_view(), name='whisky-detail'),
    path('whisky/<str:pk>/update/', views.WhiskyUpdate.as_view(), name='whisky-update'),
    path('whisky/<str:pk>/delete/', views.WhiskyDelete.as_view(), name='whisky-delete'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),


]
