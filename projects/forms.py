from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "slug", "description"]


class ProjectEditForm(ProjectForm):
    class Meta(ProjectForm.Meta):
        fields = ProjectForm.Meta.fields + ["archived", "favorite"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.id:
            self.fields["slug"].widget.attrs["readonly"] = True

    def clean_slug(self):
        instance = getattr(self, "instance", None)
        if instance and instance.id:
            return instance.slug
        else:
            return self.cleaned_data["slug"]
