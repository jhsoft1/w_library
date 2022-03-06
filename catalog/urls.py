from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('whiskies/', views.WhiskyListView.as_view(), name='whiskies'),
    path('whisky/create/', views.WhiskyCreate.as_view(), name='whisky-create'),
    path('whisky/<str:pk>', views.WhiskyDetailView.as_view(), name='whisky-detail'),
    path('whisky/<str:pk>/update/', views.WhiskyUpdate.as_view(), name='whisky-update'),
    path('whisky/<str:pk>/delete/', views.WhiskyDelete.as_view(), name='whisky-delete'),
    path('eveningwhiskies/', views.EveningWhiskyListView.as_view(), name='eveningwhiskies'),
    path('eveningwhiskies_today/', views.EveningWhiskyTodayListView.as_view(), name='eveningwhiskies-today'),
    path('eveningwhisky/<int:pk>', views.EveningWhiskyDetailView.as_view(), name='eveningwhisky-detail'),
    # path('tasting/next/', views.TastingNext.as_view(), name='next-rating'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('eveningwhisky/create/', views.EveningWhiskyCreate.as_view(), name='eveningwhisky-create'),
    path('eveningwhisky/<int:pk>/update/', views.EveningWhiskyUpdate.as_view(), name='eveningwhisky-update'),
    path('eveningwhisky/<int:pk>/delete/', views.EveningWhiskyDelete.as_view(), name='eveningwhisky-delete'),
    path('evenings/', views.EveningListView.as_view(), name='evenings'),
    path('evening/create/', views.EveningCreate.as_view(), name='evening-create'),
    path('evening/<str:pk>', views.EveningDetailView.as_view(), name='evening-detail'),
    path('evening/<str:pk>/update/', views.EveningUpdate.as_view(), name='evening-update'),
    path('evening/<str:pk>/delete/', views.EveningDelete.as_view(), name='evening-delete'),
    path('tastings/', views.TastingListView.as_view(), name='tastings'),
    path('tasting/create/', views.TastingCreate.as_view(), name='tasting-create'),
    path('tasting/create/<int:eveningwhisky>', views.TastingEveningWhiskyCreate.as_view(), name='tasting-eveningwhisky-create'),
    path('tasting/<int:pk>', views.TastingDetailView.as_view(), name='tasting-detail'),
    path('tasting/<int:pk>/update/', views.TastingUpdate.as_view(), name='tasting-update'),
    path('tasting/<int:pk>/update-value/', views.TastingValueUpdate.as_view(), name='tasting-value-update'),
    path('tasting/<int:pk>/delete/', views.TastingDelete.as_view(), name='tasting-delete'),

]
