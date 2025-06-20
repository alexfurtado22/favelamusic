from django.urls import path

from app.views import (
    ArtistCreateView,
    ArtistDeleteView,
    ArtistDetailView,  # <-- Add this
    ArtistListView,
    ArtistUpdateView,
    ProducerCreateView,
    RatingCreateView,
    RatingDeleteView,
    RatingUpdateView,
    UserProfileDetailView,
    contact_success_view,
    contact_view,
)

urlpatterns = [
    path("", ArtistListView.as_view(), name="home"),
    path("artists/create/", ArtistCreateView.as_view(), name="create_artist"),
    path("artists/<int:pk>/update/", ArtistUpdateView.as_view(), name="update_artist"),
    path("artists/<int:pk>/delete/", ArtistDeleteView.as_view(), name="delete_artist"),
    path(
        "artists/producer/create/", ProducerCreateView.as_view(), name="create_producer"
    ),
    path("contact/", contact_view, name="contact"),
    path("contact/success/", contact_success_view, name="contact_success"),
    path("users/<str:username>/", UserProfileDetailView.as_view(), name="user-profile"),
    path("artists/<int:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
    path("artists/<int:pk>/rate/", RatingCreateView.as_view(), name="artist-rate"),
    path("rating/<int:pk>/update/", RatingUpdateView.as_view(), name="rating-update"),
    path("rating/<int:pk>/delete/", RatingDeleteView.as_view(), name="rating-delete"),
]
