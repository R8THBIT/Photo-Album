from django.urls import path
from .views import (
    AlbumListView, AlbumDetailView, AlbumCreateView, 
    PhotoCreateView, AlbumUpdateView, AlbumDeleteView, RegisterView
)

urlpatterns = [
    path('', AlbumListView.as_view(), name='album_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('album/new/', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/edit/', AlbumUpdateView.as_view(), name='album_edit'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('album/<int:album_id>/photo/new/', PhotoCreateView.as_view(), name='photo_create'),
]