from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms

from .models import Advert, Resp


class AdvertAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст объявления', widget=CKEditorUploadingWidget())

    class Meta:
        model = Advert
        fields = '__all__'


class AdvertAdmin(admin.ModelAdmin):
    form = AdvertAdminForm
    model = Advert
    list_display = ('title', 'author', 'category', 'create', 'attach')


class RespAdmin(admin.ModelAdmin):
    model = Resp
    list_display = ('text', 'author', 'post', 'create', 'status')


admin.site.register(Advert, AdvertAdmin)
admin.site.register(Resp, RespAdmin)
