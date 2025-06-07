from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from app.models import Artist, Producer


class ArtistListView(ListView):
    model = Artist
    template_name = "app/home.html"
    context_object_name = "artists"


class ArtistCreateView(LoginRequiredMixin, CreateView):
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

    def form_valid(self, form):
        form.instance.creator = self.request.user  # ✅ Correct placement
        return super().form_valid(form)


class ArtistUpdateView(LoginRequiredMixin, UpdateView):
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

    def get_queryset(self):
        # Only allow updating artists created by the logged-in user
        return Artist.objects.filter(creator=self.request.user)


class ArtistDeleteView(LoginRequiredMixin, DeleteView):
    model = Artist
    template_name = "app/artist_delete.html"
    success_url = reverse_lazy("home")
    context_object_name = "artist"

    def get_queryset(self):
        return Artist.objects.filter(creator=self.request.user)


class ProducerCreateView(LoginRequiredMixin, CreateView):
    model = Producer  # ✅ Fixed from Artist
    template_name = "app/producer_create.html"
    fields = [
        "name",
        "company",
        "email",
        "website",
    ]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.creator = self.request.user  # ✅ UserProfile is the user model
        return super().form_valid(form)
