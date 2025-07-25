from django.urls import path

from app.views import (
    AddArtistToPlaylistView,
    AllBadgesView,
    # Artist and Rating
    ArtistCreateView,
    ArtistDashboardView,
    ArtistDeleteView,
    ArtistDetailView,
    ArtistListView,
    ArtistMapView,
    ArtistUpdateView,
    MarkAllAsReadView,
    NotificationListView,
    PlaylistCreateView,
    PlaylistDeleteView,
    PlaylistDetailView,
    # ✅ Playlist
    PlaylistListView,
    PlaylistUpdateView,
    ProducerCreateView,
    PublicPlaylistListView,
    RatingCreateView,
    RatingDeleteView,
    RatingUpdateView,
    TrackPlayView,
    UnreadNotificationsAPIView,
    # User Profile & Contact
    UserProfileDetailView,
    VideoPlayView,
    contact_success_view,
    contact_view,
)

from .views import FollowToggleView

urlpatterns = [
    # 🔥 Artist and Rating
    path("", ArtistListView.as_view(), name="home"),
    path("artists/create/", ArtistCreateView.as_view(), name="create_artist"),
    path("artists/<int:pk>/update/", ArtistUpdateView.as_view(), name="update_artist"),
    path("artists/<int:pk>/delete/", ArtistDeleteView.as_view(), name="delete_artist"),
    path(
        "artists/producer/create/", ProducerCreateView.as_view(), name="create_producer"
    ),
    path("artists/<int:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
    path("artists/<int:pk>/rate/", RatingCreateView.as_view(), name="artist-rate"),
    path("rating/<int:pk>/update/", RatingUpdateView.as_view(), name="rating-update"),
    path("rating/<int:pk>/delete/", RatingDeleteView.as_view(), name="rating-delete"),
    path(
        "artists/<int:pk>/dashboard/",
        ArtistDashboardView.as_view(),
        name="artist-dashboard",
    ),
    path(
        "artists/<int:artist_id>/follow/",
        FollowToggleView.as_view(),
        name="follow-toggle",
    ),
    path("artists/<int:artist_id>/play/", TrackPlayView.as_view(), name="play-track"),
    path(
        "artists/<int:artist_id>/play-video/",
        VideoPlayView.as_view(),
        name="play-video",
    ),
    path("notifications/", NotificationListView.as_view(), name="notifications-list"),
    path(
        "api/notifications/unread/",
        UnreadNotificationsAPIView.as_view(),
        name="unread-notifications-api",
    ),
    path(
        "api/notifications/mark-all-as-read/",
        MarkAllAsReadView.as_view(),
        name="mark-all-as-read",
    ),
    # 🔥 User Profile & Contact
    path("users/<str:username>/", UserProfileDetailView.as_view(), name="user-profile"),
    path("contact/", contact_view, name="contact"),
    path("contact/success/", contact_success_view, name="contact_success"),
    # 🔥 ✅ Playlists
    path("playlists/", PlaylistListView.as_view(), name="playlist-list"),
    path(
        "playlists/public/",
        PublicPlaylistListView.as_view(),
        name="public-playlist-list",
    ),
    path("playlists/create/", PlaylistCreateView.as_view(), name="playlist-create"),
    path("playlists/<int:pk>/", PlaylistDetailView.as_view(), name="playlist-detail"),
    path(
        "playlists/<int:pk>/update/",
        PlaylistUpdateView.as_view(),
        name="playlist-update",
    ),
    path(
        "playlists/<int:pk>/delete/",
        PlaylistDeleteView.as_view(),
        name="playlist-delete",
    ),
    # ✅ Add/Remove artist to/from playlist (toggle)
    path(
        "playlists/add-artist/",
        AddArtistToPlaylistView.as_view(),
        name="add-artist-to-playlist",
    ),
    path("map/", ArtistMapView.as_view(), name="artist-map"),
    path("badges/", AllBadgesView.as_view(), name="all_badges"),
]
