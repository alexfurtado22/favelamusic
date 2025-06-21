# favelamusic/app/forms.py

from django import forms

from .models import Playlist, Rating


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Your Name",
        widget=forms.TextInput(
            attrs={
                # REMOVE THIS LINE: "class": "form-input w-full rounded border-gray-300",
                "placeholder": "John Doe"
            }
        ),
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(
            attrs={
                # REMOVE THIS LINE: "class": "form-input w-full rounded border-gray-300",
                "placeholder": "you@example.com"
            }
        ),
    )
    subject = forms.CharField(
        max_length=200,
        label="Subject",
        widget=forms.TextInput(
            attrs={
                # REMOVE THIS LINE: "class": "form-input w-full rounded border-gray-300",
                "placeholder": "Subject of your message"
            }
        ),
    )
    message = forms.CharField(
        label="Your Message",
        widget=forms.Textarea(
            attrs={
                # REMOVE THIS LINE: "class": "form-textarea w-full rounded border-gray-300",
                "placeholder": "Type your message here...",
                "rows": 5,
            }
        ),
    )

    # Honeypot field (hidden from users) - Keep this as is
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value


# === ADDITION: A new form for submitting ratings ===
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["score"]
        # Optional: Make the input look like radio buttons
        widgets = {
            "score": forms.RadioSelect(
                choices=[(i, f"{i} ★") for i in range(1, 6)],
                attrs={"class": "flex items-center space-x-2"},  # Example for styling
            )
        }


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["title", "description", "is_public"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border rounded",
                    "placeholder": "Enter playlist title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2 border rounded",
                    "placeholder": "Optional description",
                    "rows": 3,
                }
            ),
            "is_public": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }
        labels = {
            "title": "Playlist Title",
            "description": "Description",
            "is_public": "Public Playlist?",
        }
