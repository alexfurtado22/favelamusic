from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db import IntegrityError  # <-- Add this import
from django.db.models import Avg, Count, Prefetch
from django.shortcuts import (
    get_object_or_404,  # <-- Add this import
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from app.models import Artist, Producer, Rating, UserProfile

from .forms import ContactForm, RatingForm  # <-- Add RatingForm import


class ArtistListView(ListView):
    model = Artist
    template_name = "app/home.html"
    context_object_name = "artists"

    def get_queryset(self):
        # This part is already correct and efficient.
        queryset = (
            super()
            .get_queryset()
            .select_related("creator", "producer", "producer__creator")
            .annotate(avg_rating=Avg("ratings__score"), num_ratings=Count("ratings"))
        )
        queryset = queryset.order_by("-avg_rating", "-num_ratings")
        return queryset

    # --- ADD THIS ENTIRE METHOD TO THE CLASS ---
    def get_context_data(self, **kwargs):
        # Get the default data
        context = super().get_context_data(**kwargs)

        # If a user is logged in...
        if self.request.user.is_authenticated:
            # ...run one single, efficient query to get their artist count...
            user_with_count = UserProfile.objects.annotate(
                artist_count_annotated=Count("artists")
            ).get(pk=self.request.user.pk)

            # ...and add the result to the template data.
            context["annotated_user"] = user_with_count

        # Return all the data to the template
        return context


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
        "youtube_link",
    ]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.creator = self.request.user  # ✅ Correct placement
        return super().form_valid(form)


class ArtistUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
        "youtube_link",
    ]
    success_url = reverse_lazy("home")
    context_object_name = "artist"

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().creator

    def get_queryset(self):
        # Only allow updating artists created by the logged-in user
        return Artist.objects.filter(creator=self.request.user)


class ArtistDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Artist
    template_name = "app/artist_delete.html"
    success_url = reverse_lazy("home")
    context_object_name = "artist"

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().creator

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


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            from_email_user = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            email_subject_to_you = (
                f"Contact Form: {subject} from {name} ({from_email_user})"
            )
            email_body_to_you = (
                f"Name: {name}\nEmail: {from_email_user}\n\nMessage:\n{message}"
            )

            try:
                send_mail(
                    email_subject_to_you,
                    email_body_to_you,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,  # Keep False for development to catch errors
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect("contact_success")
            except Exception as e:
                # --- Optional: Enable logging in production ---
                # import logging
                # logger = logging.getLogger(__name__)
                # logger.exception("Error sending contact form email:")
                # -----------------------------------------------

                messages.error(
                    request,
                    f"There was an error sending your message. Please try again later. Error: {e}",
                )
        else:
            # --- IMPROVEMENT HERE ---
            # Check if the honeypot field specifically caused the validation failure
            if "honeypot" in form.errors:
                messages.error(
                    request,
                    "Your message could not be sent due to suspected spam activity. Please try again or contact us directly if you believe this is an error.",
                )
            else:
                # For other validation errors (e.g., missing required fields)
                messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, "app/contact.html", {"form": form})


def contact_success_view(request):
    return render(request, "app/contact_success.html")


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = "app/userprofile_detail.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .annotate(artist_count_annotated=Count("artists"))
            # === THIS IS THE CORRECTED LINE ===
            .prefetch_related(
                Prefetch(
                    "artists",
                    queryset=Artist.objects.select_related("producer", "creator"),
                )
            )
        )
        return queryset


# app/views.py


# app/views.py


# app/views.py


class ArtistDetailView(DetailView):
    model = Artist
    template_name = "app/artist_detail.html"
    context_object_name = "artist"

    def get_queryset(self):
        # This queryset is perfect. No changes needed here.
        return (
            super()
            .get_queryset()
            .select_related("creator", "producer")
            .annotate(
                avg_rating=Avg("ratings__score"),
                num_ratings=Count("ratings"),
            )
            .prefetch_related("ratings__user")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.object

        # === THIS IS THE FINAL OPTIMIZATION ===
        user_rating = None
        if self.request.user.is_authenticated:
            # Instead of a new query, we loop through the ratings that
            # were already fetched by prefetch_related. This is instant.
            for rating in artist.ratings.all():  # This uses the prefetched cache
                if rating.user_id == self.request.user.id:
                    user_rating = rating
                    break  # We found it, no need to keep looping

        context["user_rating"] = user_rating
        context["rating_form"] = RatingForm()
        return context


# === ADDITION: A view to process the rating form submission ===
class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm

    def form_valid(self, form):
        # Get the artist object from the URL
        artist = get_object_or_404(Artist, pk=self.kwargs["pk"])

        # Assign the artist and logged-in user to the rating
        form.instance.artist = artist
        form.instance.user = self.request.user

        try:
            # Try to save the rating
            messages.success(self.request, f"Thank you for rating {artist.name}!")
            return super().form_valid(form)
        except IntegrityError:
            # This happens if the user already rated this artist
            messages.warning(self.request, f"You have already rated {artist.name}.")
            return redirect("artist-detail", pk=artist.pk)

    def get_success_url(self):
        return reverse_lazy("home")


class RatingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = "app/rating_form.html"

    def get_queryset(self):
        return (
            super().get_queryset().select_related("user", "artist", "artist__creator")
        )

    def get_object(self, queryset=None):
        if not hasattr(self, "_cached_object"):
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        rating = self.get_object()
        return self.request.user == rating.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm(instance=self.object)  # Pre-fill the form

        user = self.request.user
        if user.is_authenticated:
            user_rating = self.object.artist.ratings.filter(
                user=user
            ).first()  # Correct: through artist
        else:
            user_rating = None

        context["user_rating"] = user_rating
        return context

    def get_success_url(self):
        return reverse_lazy("home")


# === ADDITION: View to delete a rating ===
class RatingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rating
    template_name = "app/rating_confirm_delete.html"

    def get_queryset(self):
        # Join related user and artist to reduce extra queries
        return (
            super().get_queryset().select_related("user", "artist", "artist__creator")
        )

    def get_object(self, queryset=None):
        if not hasattr(self, "_cached_object"):
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        rating = self.get_object()
        return self.request.user == rating.user

    def get_success_url(self):
        return reverse_lazy("home")
