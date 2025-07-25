from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .models import Artist, Badge, Follower, Notification, UserBadge


@receiver(post_save, sender=Follower)
def send_new_follower_notification(sender, instance, created, **kwargs):
    """
    Sends a notification to an artist when a new user follows them.
    """
    if created:
        artist_creator = instance.artist.creator
        follower_user = instance.user

        if artist_creator != follower_user:
            message = f"<b>{follower_user.username}</b> started following your artist <b>{instance.artist.name}</b>."
            url = reverse("user-profile", kwargs={"username": follower_user.username})

            # Create the notification in the database with the new fields
            Notification.objects.create(
                user=artist_creator,
                sender=follower_user,
                message=message,
                url=url,
                notification_type=Notification.NotificationType.NEW_FOLLOWER,
            )

            # Send the real-time notification with sender info for the avatar
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"notifications_{artist_creator.id}",
                {
                    "type": "notify",
                    "message": message,
                    "url": url,
                    "sender_username": follower_user.username,
                    # Assumes you have an 'avatar' field on your UserProfile model
                    "sender_avatar_url": follower_user.avatar.url
                    if hasattr(follower_user, "avatar") and follower_user.avatar
                    else None,
                },
            )


@receiver(post_save, sender=Artist)
def update_user_badges_on_artist_creation(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.creator
    artist_count = user.artists.count()

    earned_badge_ids = UserBadge.objects.filter(user=user).values_list(
        "badge_id", flat=True
    )
    available_badges = Badge.objects.exclude(id__in=earned_badge_ids)

    for badge in available_badges:
        if artist_count >= badge.required_artist_count:
            UserBadge.objects.create(user=user, badge=badge)
            print(f"🎉 Badge '{badge.name}' awarded to {user.username}")
