from django import forms

from .models import Timer
from .services import get_active_timer, clear_active_timer


class TimerForm(forms.ModelForm):
    class Meta:
        model = Timer
        fields = ["project", "start", "stop"]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        active = get_active_timer(self.user)

        if active is not None and cleaned_data["stop"] is None:
            if active.start > cleaned_data["start"]:
                raise forms.ValidationError(
                    f"Cannot create active timer before {active.start}"
                )

        return cleaned_data
