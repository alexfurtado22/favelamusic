# favelamusic/app/forms.py

from django import forms


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
