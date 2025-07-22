from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import IntegrityError  # <-- Add this import
from django.db.models import Avg, Count, Exists, F, OuterRef, Prefetch, Window
from django.db.models.functions import Rank, TruncDate
from django.http import JsonResponse
from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,  # <-- Add this import
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from app.models import (
    Artist,
    Follower,
    Notification,
    Playlist,
    Producer,
    Rating,
    TrackPlay,
    UserProfile,
    VideoPlay,
)

from .forms import ContactForm, PlaylistForm, RatingForm  # <-- Add RatingForm import


class ArtistListView(ListView):
    model = Artist
    template_name = "app/home.html"
    context_object_name = "artists"
    paginate_by = 6

    def get_queryset(self):
        # Start with the base queryset and prefetch related data
        queryset = (
            super()
            .get_queryset()
            .select_related("creator", "producer")
            .annotate(avg_rating=Avg("ratings__score"), num_ratings=Count("ratings"))
        )

        # ✨ ADDITION: Annotate with follow status for the logged-in user
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_following=Exists(
                    Follower.objects.filter(
                        user=self.request.user, artist=OuterRef("pk")
                    )
                )
            )

        # Handle search functionality
        search_term = self.request.GET.get("q")
        if search_term:
            search_vector = (
                SearchVector("name", weight="A")
                + SearchVector("genre", weight="B")
                + SearchVector("creator__username", weight="C")
            )
            search_query = SearchQuery(search_term)
            queryset = (
                queryset.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query),
                )
                .filter(rank__gte=0.2)
                .order_by("-rank", "-avg_rating", "-num_ratings")
            )
        else:
            # Default ordering when not searching
            queryset = queryset.order_by("-avg_rating", "-num_ratings")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["range_100"] = range(1, 101)
        if self.request.user.is_authenticated:
            user_with_count = UserProfile.objects.annotate(
                artist_count_annotated=Count("artists")
            ).get(pk=self.request.user.pk)
            context["annotated_user"] = user_with_count
        context["search_term"] = self.request.GET.get("q", "")
        return context


class ArtistCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
    success_message = "Artist '%(name)s' created successfully!"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ArtistUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
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
    success_message = "Artist '%(name)s' updated successfully!"

    def get_queryset(self):
        return Artist.objects.filter(creator=self.request.user).select_related(
            "creator", "producer"
        )

    def get_object(self, queryset=None):
        if not hasattr(self, "_cached_object"):
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        return self.request.user == self.get_object().creator


# app/views.py


class ArtistDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView, SuccessMessageMixin
):
    model = Artist
    template_name = "app/artist_delete.html"
    success_url = reverse_lazy("home")
    success_message = "Artist '%(name)s' deleted successfully!"
    context_object_name = "artist"

    def get_queryset(self):
        """
        Filters artists for the current user and uses select_related('creator')
        to fetch the related User object in the same database query. This
        avoids the N+1 query problem when creator is accessed later.
        """
        return (
            super()
            .get_queryset()
            .select_related("creator")
            .filter(creator=self.request.user)
        )

    def get_object(self, queryset=None):
        """
        Caches the retrieved object on the view instance (`self.object`)
        to prevent multiple database lookups.

        The first time this method is called (from test_func), it fetches
        the object from the database. Subsequent calls will return the cached
        object directly.
        """
        if not hasattr(self, "object"):
            self.object = super().get_object(queryset)
        return self.object

    def test_func(self):
        """
        This test now uses the efficient get_object method. The first call here
        fetches and caches the object. The subsequent call within the view's
        GET or POST handler will use the cache.
        """
        return self.request.user == self.get_object().creator


class ProducerCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = Producer  # ✅ Fixed from Artist
    template_name = "app/producer_create.html"
    fields = [
        "name",
        "company",
        "email",
        "website",
    ]
    success_url = reverse_lazy("create_artist")
    success_message = "Producer '%(name)s' created successfully!"

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


class ArtistDetailView(DetailView):
    model = Artist
    template_name = "app/artist_detail.html"
    context_object_name = "artist"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("creator", "producer")
            .annotate(
                avg_rating=Avg("ratings__score"),
                num_ratings=Count("ratings"),
            )
            .prefetch_related(
                "ratings__user",  # Ratings
                "playlists",  # Playlists that include this artist
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.object

        # Optimized lookup for current user's rating (already cached)
        user_rating = None
        if self.request.user.is_authenticated:
            for rating in artist.ratings.all():
                if rating.user_id == self.request.user.id:
                    user_rating = rating
                    break

            # ✅ Get the user's playlists for the Add/Remove buttons
            user_playlists = Playlist.objects.filter(user=self.request.user).order_by(
                "title"
            )
        else:
            user_playlists = Playlist.objects.none()

        context["user_rating"] = user_rating
        context["rating_form"] = RatingForm()
        context["user_playlists"] = user_playlists  # ✅ New line

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

    def form_valid(self, form):
        # Manually create the success message
        messages.success(
            self.request,
            f"Your rating for '{self.object.artist.name}' has been updated successfully.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("artist-detail", kwargs={"pk": self.object.artist.pk})


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
        """
        Redirects the user back to the artist's detail page after
        successfully deleting a rating.
        """
        return reverse_lazy("artist-detail", kwargs={"pk": self.object.artist.pk})

    def post(self, request, *args, **kwargs):
        """
        Manually create a success message before the object is deleted.
        """
        # Get the object before it's deleted to use its name in the message
        rating_object = self.get_object()
        messages.success(
            self.request,
            f"Your rating for '{rating_object.artist.name}' has been deleted.",
        )
        return super().post(request, *args, **kwargs)


class PlaylistListView(LoginRequiredMixin, ListView):
    # ... your other class attributes

    def get_queryset(self):
        # Add select_related("user") to the query
        return (
            Playlist.objects.select_related("user")
            .filter(user=self.request.user)
            .annotate(num_artists=Count("artists"))
            .prefetch_related("artists")
        )


class PublicPlaylistListView(ListView):
    """
    Displays a list of all playlists that are marked as public.
    """

    model = Playlist
    template_name = "app/public_playlist_list.html"
    context_object_name = "playlists"

    def get_queryset(self):
        return (
            Playlist.objects.filter(is_public=True)
            .annotate(num_artists=Count("artists"))
            .select_related("user")
            .prefetch_related("artists")
        )


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = "app/playlist_detail.html"
    context_object_name = "playlist"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = Playlist.objects.select_related("user").prefetch_related(
                Prefetch(
                    "artists",
                    queryset=Artist.objects.select_related("producer").annotate(
                        avg_rating=Avg("ratings__score"), num_ratings=Count("ratings")
                    ),
                )
            )
        return queryset.get(pk=self.kwargs["pk"])


class PlaylistCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    """
    Handles the creation of a new playlist.
    """

    model = Playlist
    form_class = PlaylistForm
    template_name = "app/playlist_form.html"
    success_url = reverse_lazy("playlist-list")
    success_message = "Playlist '%(title)s' was created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlaylistUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView, SuccessMessageMixin
):
    """
    Handles updating an existing playlist.
    """

    model = Playlist
    form_class = PlaylistForm
    template_name = "app/playlist_form.html"
    success_url = reverse_lazy("playlist-list")
    success_message = "Playlist '%(title)s' was updated successfully."

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user


class PlaylistDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView, SuccessMessageMixin
):
    """
    Handles the deletion of a playlist after confirmation.
    """

    model = Playlist
    template_name = "app/playlist_confirm_delete.html"
    success_url = reverse_lazy("playlist-list")
    success_message = "Playlist '%(title)s' was deleted."

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user


class AddArtistToPlaylistView(LoginRequiredMixin, View):
    """
    Handles the POST request to add or remove an artist from a user's playlist.
    """

    def post(self, request, *args, **kwargs):
        artist_id = request.POST.get("artist_id")
        playlist_id = request.POST.get("playlist_id")

        artist = get_object_or_404(Artist, id=artist_id)
        playlist = get_object_or_404(
            Playlist.objects.prefetch_related("artists"),
            id=playlist_id,
            user=request.user,
        )

        # Toggle the artist's existence in the playlist
        if artist in playlist.artists.all():
            playlist.artists.remove(artist)
            messages.info(
                request, f"Removed '{artist.name}' from playlist '{playlist.title}'."
            )
        else:
            playlist.artists.add(artist)
            messages.success(
                request, f"Added '{artist.name}' to playlist '{playlist.title}'."
            )

        return redirect("artist-detail", pk=artist_id)


class ArtistDashboardView(LoginRequiredMixin, DetailView):
    model = Artist
    template_name = "app/artist_dashboard.html"
    context_object_name = "artist"

    def get_queryset(self):
        # OPTIMIZATION: Annotate the main artist object with counts.
        # This data will be fetched in the initial query for the artist.
        return Artist.objects.filter(creator=self.request.user).annotate(
            playlist_count=Count("playlists", distinct=True),
            follower_count=Count("followers", distinct=True),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Use `self.object` which is already fetched by the DetailView.
        artist = self.object

        # --- Chart Data Preparation (Already efficient) ---
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        date_range = [thirty_days_ago + timedelta(days=i) for i in range(31)]

        follower_counts = {
            item["day"]: item["count"]
            for item in Follower.objects.filter(
                artist=artist, created_at__date__gte=thirty_days_ago
            )
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
        }

        play_counts = {
            item["day"]: item["count"]
            for item in TrackPlay.objects.filter(
                artist=artist, played_at__date__gte=thirty_days_ago
            )
            .annotate(day=TruncDate("played_at"))
            .values("day")
            .annotate(count=Count("id"))
        }

        video_play_counts = {
            item["day"]: item["count"]
            for item in VideoPlay.objects.filter(
                artist=artist, played_at__date__gte=thirty_days_ago
            )
            .annotate(day=TruncDate("played_at"))
            .values("day")
            .annotate(count=Count("id"))
        }

        chart_labels = [day.strftime("%b %d") for day in date_range]
        context["chart_labels"] = chart_labels
        context["follower_chart_data"] = [
            follower_counts.get(day, 0) for day in date_range
        ]
        context["play_chart_data"] = [play_counts.get(day, 0) for day in date_range]
        context["video_play_chart_data"] = [
            video_play_counts.get(day, 0) for day in date_range
        ]

        # --- Stat Card Preparation ---
        context["playlist_appearances"] = artist.playlist_count

        # --- ✨ FINAL OPTIMIZATION: Genre-wide Statistics ---
        # Get all artists in the same genre once.
        genre_artists = Artist.objects.filter(genre=artist.genre)

        # Perform one single query for all genre-level aggregates.
        genre_aggregates = genre_artists.aggregate(
            total_followers=Count("followers", distinct=True),
            total_plays=Count("plays", distinct=True),
            total_video_plays=Count("video_plays", distinct=True),
            total_artists=Count("id", distinct=True),
        )
        total_artists_in_genre = genre_aggregates.get("total_artists", 0)
        context["total_in_genre"] = total_artists_in_genre

        # Calculate averages in Python, avoiding extra queries.
        if total_artists_in_genre > 0:
            context["genre_avg_followers"] = (
                genre_aggregates.get("total_followers", 0) / total_artists_in_genre
            )
        else:
            context["genre_avg_followers"] = 0

        context["total_genre_plays"] = genre_aggregates.get("total_plays", 0)
        context["total_genre_video_plays"] = genre_aggregates.get(
            "total_video_plays", 0
        )

        # Perform a second, separate query just to get the rank for the specific artist.
        # This is now the only other query needed for genre stats.
        try:
            ranked_artist = (
                genre_artists.annotate(f_count=Count("followers"))
                .annotate(rank=Window(expression=Rank(), order_by=F("f_count").desc()))
                .get(pk=artist.pk)
            )
            context["genre_rank"] = ranked_artist.rank
        except Artist.DoesNotExist:
            context["genre_rank"] = "N/A"

        return context


class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, artist_id):
        artist = get_object_or_404(Artist, id=artist_id)
        follower, created = Follower.objects.get_or_create(
            user=request.user, artist=artist
        )
        if not created:
            follower.delete()
        # Redirect back to the page the user was on.
        return redirect(request.META.get("HTTP_REFERER", "home"))


class TrackPlayView(View):
    """
    This view does two things on a GET request:
    1. Creates a TrackPlay record in the database for the given artist.
    2. Redirects the user to the actual URL of the MP3 file.
    """

    def get(self, request, artist_id):
        artist = get_object_or_404(Artist, id=artist_id)

        # Log the track play. Link it to the user if they are logged in.
        TrackPlay.objects.create(
            artist=artist, user=request.user if request.user.is_authenticated else None
        )

        # Redirect to the actual file URL so the browser can play it.
        return HttpResponseRedirect(artist.track.url)


# app/views.py

# app/views.py


class VideoPlayView(View):
    def get(self, request, artist_id):
        artist = get_object_or_404(Artist, id=artist_id)

        # Create the VideoPlay record
        VideoPlay.objects.create(
            artist=artist, user=request.user if request.user.is_authenticated else None
        )

        # FIX: Redirect to the video file, not the track
        return HttpResponseRedirect(artist.video.url)


class UnreadNotificationsAPIView(LoginRequiredMixin, View):
    """API endpoint for fetching paginated unread notifications."""

    def get(self, request, *args, **kwargs):
        notifications_query = request.user.notifications.filter(
            is_read=False
        ).select_related("sender")

        paginator = Paginator(notifications_query, 10)  # Show 10 notifications per page
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        data = [
            {
                "id": n.id,
                "sender_avatar_url": n.sender.avatar.url
                if hasattr(n.sender, "avatar") and n.sender.avatar
                else None,
                "message": n.message,
                "url": n.url,
                "created_at": n.created_at.isoformat(),
            }
            for n in page_obj
        ]

        return JsonResponse({"notifications": data, "has_more": page_obj.has_next()})


class NotificationListView(LoginRequiredMixin, ListView):
    """A page to display all of a user's notifications."""

    model = Notification
    template_name = "app/notifications_list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        # Mark all as read when visiting the full page
        self.request.user.notifications.update(is_read=True)
        return self.request.user.notifications.all().select_related("sender")


class MarkAllAsReadView(LoginRequiredMixin, View):
    def post(self, request):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return JsonResponse({"status": "success"})
