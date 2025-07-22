import os
import re

import filetype
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.db import models
from django.db.models import Avg

GENRE_MUSIC = (
    ("Rock", "Rock"),
    ("Pop", "Pop"),
    ("Classical", "Classical"),
    ("Electronic", "Electronic"),
    ("Jazz", "Jazz"),
    ("Folk", "Folk"),
    ("Hip-Hop / Rap", "Hip-Hop / Rap"),
    ("Soul", "Soul"),
    ("Country", "Country"),
    ("World / Regional", "World / Regional"),
    ("Other", "Other"),
)


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)  # unique and required by default

    REQUIRED_FIELDS = ["email"]

    @property
    def artist_count(self):
        return self.artists.count()

    def __str__(self):
        return self.username


class Producer(models.Model):
    name = models.CharField(max_length=65)
    company = models.CharField(max_length=55)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "company", "creator"],
                name="unique_producer_name_company_creator",
            )
        ]

    def __str__(self):
        return self.name


def validate_image(image):
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError(
            "The image file is too large. Maximum size allowed is 2 MB."
        )

    kind = filetype.guess(image)
    if kind is None or kind.mime not in ["image/jpeg", "image/png"]:
        raise ValidationError("Only JPEG and PNG image files are allowed.")


def validate_video_file(video):
    max_size = 20 * 1024 * 1024
    if video.size > max_size:
        raise ValidationError("Video file too large (max 20 MB).")

    ext = os.path.splitext(video.name)[1].lower()

    initial_pos = video.tell()
    video.seek(0)
    kind = filetype.guess(video.read(261))
    video.seek(initial_pos)

    if kind is None or kind.mime != "video/mp4" or ext != ".mp4":
        raise ValidationError("Only .mp4 video files are allowed.")


def validate_mp3_file(file):
    max_size = 10 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError("Audio file too large (max 10 MB).")

    ext = os.path.splitext(file.name)[1].lower()
    kind = filetype.guess(file)

    if kind is None:
        raise ValidationError(
            "Could not determine file type. Only .mp3 audio files are allowed."
        )

    if kind.mime != "audio/mpeg" or ext != ".mp3":
        raise ValidationError("Only .mp3 audio files are allowed.")


# --- New/Improved URL Validators ---


def validate_twitter_url(value):
    try:
        URLValidator()(value)  # Basic URL validation
    except ValidationError:
        raise ValidationError("Please enter a valid URL.")

    # More specific check to ensure it's a Twitter URL (handles various subdomains like x.com)
    if not re.match(
        r"^(https?://)?(www\.)?(twitter\.com|x\.com)/[a-zA-Z0-9_]+/?$", value
    ):
        raise ValidationError("Enter a valid Twitter URL.")


def validate_instagram_url(value):
    try:
        URLValidator()(value)  # Basic URL validation
    except ValidationError:
        raise ValidationError("Please enter a valid URL.")

    # More specific check to ensure it's an Instagram URL
    if not re.match(r"^(https?://)?(www\.)?instagram\.com/[a-zA-Z0-9_.]+$", value):
        raise ValidationError("Enter a valid Instagram URL.")


def validate_youtube_url(value):
    try:
        URLValidator()(value)  # Basic URL validation
    except ValidationError:
        raise ValidationError("Please enter a valid URL.")

    # Use a raw string (r"...") to avoid syntax warnings
    youtube_regex = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})([?&].*)?|(https?://)?(www\.)?youtube\.com/playlist\?list=([^&=%\?]+)"

    if not re.match(youtube_regex, value):
        raise ValidationError("Please enter a valid YouTube video or playlist URL.")

    if not re.match(youtube_regex, value):
        raise ValidationError("Please enter a valid YouTube video or playlist URL.")


class Artist(models.Model):
    name = models.CharField(max_length=65)
    picture = models.ImageField(
        upload_to="profile", null=True, blank=True, validators=[validate_image]
    )
    track = models.FileField(
        upload_to="tracks", null=False, blank=False, validators=[validate_mp3_file]
    )
    video = models.FileField(
        upload_to="videos", null=True, blank=True, validators=[validate_video_file]
    )
    youtube_link = models.URLField(
        blank=True, null=True, validators=[validate_youtube_url]
    )
    genre = models.CharField(
        max_length=20, choices=GENRE_MUSIC, default="Hip-Hop / Rap", db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="artists"
    )
    producer = models.ForeignKey(
        Producer, null=True, blank=True, on_delete=models.SET_NULL
    )
    content = models.TextField(blank=True, default="")
    twitter = models.URLField(blank=True, validators=[validate_twitter_url])
    instagram = models.URLField(blank=True, validators=[validate_instagram_url])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # === ADDITION: A property to calculate the average rating ===
    @property
    def average_rating(self):
        # Calculates the average score of all ratings, returns 0 if none exist.
        return self.ratings.aggregate(Avg("score"))["score__avg"] or 0

    def __str__(self):
        return self.name


# === ADDITION: The new model to store ratings ===
class Rating(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only rate an artist once
        constraints = [
            models.UniqueConstraint(
                fields=["user", "artist"], name="unique_user_artist_rating"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.score} stars for {self.artist.name} by {self.user.username}"


class Playlist(models.Model):
    title = models.CharField(max_length=150)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="playlists"
    )
    artists = models.ManyToManyField(Artist, related_name="playlists", blank=True)
    description = models.TextField(
        blank=True, help_text="Optional description of the playlist."
    )
    is_public = models.BooleanField(
        default=False, help_text="If checked, anyone can view this playlist."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "title"], name="unique_user_playlist_title"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    @property
    def artist_count(self):
        return self.artists.count()


class Follower(models.Model):
    """Represents a user following an artist."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "artist"], name="unique_user_artist_follow"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} follows {self.artist.name}"


class TrackPlay(models.Model):
    """Logs an instance of a track being played."""

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="plays")
    # You can optionally link this to a user if they are logged in
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    played_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Track for {self.artist.name} played at {self.played_at}"


# app/models.py


class VideoPlay(models.Model):
    """Logs an instance of a video being played."""

    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="video_plays"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    played_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Video for {self.artist.name} played at {self.played_at}"


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        NEW_FOLLOWER = "new_follower", "New Follower"
        NEW_RATING = "new_rating", "New Rating"
        PLAYLIST_ADD = "playlist_add", "Playlist Add"
        SYSTEM = "system", "System"

    # The user who receives the notification
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    # The user who triggered the notification (optional)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notifications",
    )

    message = models.TextField()
    notification_type = models.CharField(
        max_length=20, choices=NotificationType.choices
    )
    url = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"
