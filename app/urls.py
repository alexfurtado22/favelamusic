from django.urls import path

from app.views import (
    ArtistCreateView,
    ArtistDeleteView,
    ArtistListView,
    ArtistUpdateView,
)

urlpatterns = [
    path("", ArtistListView.as_view(), name="home"),
    path("artists/create/", ArtistCreateView.as_view(), name="create_artist"),
    path("artists/<int:pk>/update/", ArtistUpdateView.as_view(), name="update_artist"),
    path("artists/<int:pk>/delete/", ArtistDeleteView.as_view(), name="delete_artist"),
]
