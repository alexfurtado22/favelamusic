from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from django.utils.html import format_html

from app.models import Artist, Producer, Rating, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    # --- (Your fieldsets remain the same) ---
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    # --- END of unchanged fieldsets ---

    # 3. CHANGED: Use a new method name here instead of "artist_count"
    list_display = ("username", "email", "is_staff", "is_active", "get_artist_count")
    search_fields = ("username", "email")
    ordering = ("username",)

    # 4. ADDED: The get_queryset method to perform the efficient query
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_artist_count=Count("artists", distinct=True))
        return queryset

    # 5. ADDED: The method to display the pre-calculated count
    def get_artist_count(self, obj):
        return obj._artist_count

    # This makes the column header nice and allows sorting
    get_artist_count.short_description = "Artist Count"
    get_artist_count.admin_order_field = "_artist_count"


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "creator", "email", "website")
    search_fields = ("name", "company", "creator__username")
    list_filter = ("company",)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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

    # 👇 Control the field order in the form
    fields = (
        "name",
        "picture",
        "track",
        "video",
        # now comes after video
        "genre",
        "producer",
        "content",
        "instagram",
        "youtube_link",
        "twitter",
        "creator",
        "created_at",
        "updated_at",
        "picture_preview",
        "track_preview",
        "video_preview",
    )

    # Media preview methods
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


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("artist", "user", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("artist__name", "user__username")
    readonly_fields = ("created_at",)
