from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from app.models import Artist, Producer

from .forms import ContactForm


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
