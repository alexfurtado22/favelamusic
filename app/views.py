from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from app.models import Artist


class ArtistListView(ListView):
    model = Artist
    template_name = "app/home.html"
    context_object_name = "artists"


class ArtistCreateView(CreateView):
    model = Artist
    template_name = "app/artist_create.html"
    fields = [
        "name",
        "picture",
        "track",
        "video",
        "genre",
        "content",
        "producer",
        "twitter",
        "instagram",
    ]
    success_url = reverse_lazy("home")


class ArtistUpdateView(UpdateView):
    model = Artist
    template_name = "app/artist_update.html"
    fields = [
        "name",
        "picture",
        "track",
        "video",
        "genre",
        "content",
        "producer",
        "twitter",
        "instagram",
    ]
    success_url = reverse_lazy("home")
    context_object_name = "artist"


class ArtistDeleteView(DeleteView):
    model = Artist
    template_name = "app/artist_delete.html"
    success_url = reverse_lazy("home")
    context_object_name = "artist"
