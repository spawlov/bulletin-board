from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Advert, Resp


class AdvertForm(forms.ModelForm):
    """Добавление публикации на сайт"""
    text = forms.CharField(label='Текст объявления', widget=CKEditorUploadingWidget())
    error_css_class = 'text-danger fw-semibold'

    class Meta:
        model = Advert
        fields = ('title', 'text', 'category', 'attach',)
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'text': forms.Textarea(
                attrs={'class': 'form-control'}
            ),
            'category': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'attach': forms.FileInput(
                attrs={'class': 'form-control'},
            ),
        }


class RespForm(forms.ModelForm):
    """Добавление отклика"""
    error_css_class = 'text-danger fw-semibold'

    class Meta:
        model = Resp
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control'},
            ),
        }
