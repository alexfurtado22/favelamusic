from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from app.models import Artist, Producer, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    # Combine all desired fields into a single list_display
    list_display = ("username", "email", "is_staff", "is_active", "artist_count")
    search_fields = ("username", "email")
    # You can specify ordering
    ordering = ("username",)


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "creator", "email", "website")
    search_fields = ("name", "company", "creator__username")
    list_filter = ("company",)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "genre",
        "creator",
        "producer",
        "picture_preview",
        "track_preview",
        "video_preview",
        "created_at",
    )
    ordering = ("created_at",)
    search_fields = ("name", "genre", "creator__username", "producer__name")
    list_filter = ("genre", "creator", "producer")
    date_hierarchy = "created_at"
    readonly_fields = (
        "created_at",
        "updated_at",
        "picture_preview",
        "track_preview",
        "video_preview",
    )

    # Methods for previewing media (as before)
    def picture_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.picture.url,
            )
        return "-"

    picture_preview.short_description = "Picture"

    def track_preview(self, obj):
        if obj.track:
            return format_html(
                '<audio controls style="max-width: 200px;">'
                '<source src="{}" type="audio/mpeg">'
                "Your browser does not support the audio element."
                "</audio>",
                obj.track.url,
            )
        return "-"

    track_preview.short_description = "Track"

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video controls style="max-width: 200px;">'
                '<source src="{}" type="video/mp4">'
                "Your browser does not support the video element."
                "</video>",
                obj.video.url,
            )
        return "-"

    video_preview.short_description = "Video"
