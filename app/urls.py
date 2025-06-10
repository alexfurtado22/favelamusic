from django.urls import path

from app.views import (
    ArtistCreateView,
    ArtistDeleteView,
    ArtistListView,
    ArtistUpdateView,
    ProducerCreateView,
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
]
