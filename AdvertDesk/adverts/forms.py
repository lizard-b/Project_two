from django import forms
from django.core.exceptions import ValidationError
from .models import Advert, Response


class AdvertCreateForm(forms.ModelForm):
    title = forms.CharField(min_length=20)

    class Meta:
        model = Advert
        fields = ['title', 'slug', 'content', 'short_content', 'category', 'thumbnail', 'status']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Advert content should not be the same as it's title."
            )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['short_content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False
        self.fields['short_content'].required = False


class ResponseCreateForm(forms.ModelForm):
    """
    Форма добавления отклика
    """
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    response_text = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Отклик', 'class': 'form-control'}))

    class Meta:
        model = Response
        fields = ('response_text',)

