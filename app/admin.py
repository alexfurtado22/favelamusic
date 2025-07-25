from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from django.utils.html import format_html

from app.models import Artist, Badge, Producer, Rating, UserBadge, UserProfile


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
        # Adicionados campos de localização à lista
        "location_name",
        "latitude",
        "longitude",
        "created_at",
    )
    ordering = ("-created_at",)
    search_fields = (
        "name",
        "genre",
        "creator__username",
        "producer__name",
        "location_name",
    )
    list_filter = ("genre", "creator", "producer")
    date_hierarchy = "created_at"
    readonly_fields = (
        "created_at",
        "updated_at",
        "picture_preview",
        "track_preview",
        "video_preview",
    )

    # Uso de fieldsets para uma melhor organização do formulário de edição
    fieldsets = (
        (
            "Main Information",
            {"fields": ("name", "creator", "producer", "genre", "content")},
        ),
        (
            "Location",
            {
                "fields": ("location_name", "latitude", "longitude"),
                "description": "You can manually enter coordinates or use the 'Get Current Location' button on the main site's creation form.",
            },
        ),
        (
            "Media Files",
            {
                "fields": (
                    "picture",
                    "picture_preview",
                    "track",
                    "track_preview",
                    "video",
                    "video_preview",
                ),
            },
        ),
        (
            "Social Links",
            {
                "fields": ("instagram", "youtube_link", "twitter"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),  # Torna esta secção recolhível
            },
        ),
    )

    # Media preview methods (o seu código original está perfeito)
    def picture_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.picture.url,
            )
        return "-"

    picture_preview.short_description = "Picture Preview"

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

    track_preview.short_description = "Track Preview"

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

    video_preview.short_description = "Video Preview"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("artist", "user", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("artist__name", "user__username")
    readonly_fields = ("created_at",)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Badge model.
    """

    list_display = ("name", "icon", "required_artist_count", "description")
    search_fields = ("name", "description")
    list_filter = ("required_artist_count",)
    ordering = ("required_artist_count",)


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserBadge model.
    This model is typically managed by signals, so making it read-only is often best.
    """

    list_display = ("user", "badge", "awarded_at")
    search_fields = ("user__username", "badge__name")
    list_filter = ("badge", "awarded_at")
    ordering = ("-awarded_at",)

    # Make the fields read-only since they are awarded automatically
    readonly_fields = ("user", "badge", "awarded_at")

    def has_add_permission(self, request):
        # Prevent admins from manually adding UserBadge instances
        return False

    def has_change_permission(self, request, obj=None):
        # Allow viewing but not changing
        return False
